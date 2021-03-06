from celery import task, current_task
from imposm.parser import OSMParser
import json
import os.path
import sys
import random
import datetime
from django.utils.timezone import utc

from .models import KircheOsm, Ref

def set_tags(kosm, dtags):
    if 'name' in dtags:
        kosm.name = dtags['name']
        del dtags['name']
    if 'religion' in dtags:
        kosm.religion = dtags['religion']
        del dtags['religion']
    if 'denomination' in dtags:
        kosm.denomination = dtags['denomination']
        del dtags['denomination']
    del dtags['amenity']
    kosm.addional_fields = json.dumps(dtags)
    return kosm


@task
def insert_church_node(data):
    kosm, created = KircheOsm.objects.get_or_create(osm_id=data['id'])

    kosm.lon = data['refs'][0]
    kosm.lat = data['refs'][1]

    kosm = set_tags(kosm, data.get('tags'))
    kosm.osm_type = 'N'

    # set mpoly and point in dataset
    kosm.set_geo()
    kosm.save()
    return True


@task(default_retry_delay=10*60, max_retries=100)
def insert_church_way(data):
    """ Insert church based on way(s).
    Needs references to points for creating the way(s)
    """
    # are all refs in database?
    ref_tuples = []
    for ref in data.get('refs'):
        try:
            x = Ref.objects.get(osm_id=ref)
        except Ref.DoesNotExist:
            x = None
        except Ref.MultipleObjectsReturned:
            x = Ref.objects.filter(osm_id=ref)
            x[1].delete()
            x = x[0]

        if x and not x.need_update:
            ref_tuples.append(x.point.tuple)
        else:
            # not yet done / postpone
            return current_task.retry(countdown=600)

    try:
        kosm, created = KircheOsm.objects.get_or_create(osm_id=data['id'])
    except KircheOsm.MultipleObjectsReturned:
        x = KircheOsm.objects.filter(osm_id=data['id'])
        x[1].delete()
        kosm = x[0]

    kosm = set_tags(kosm, data.get('tags'))
    kosm.osm_type = 'W'

    try:
        kosm.mpoly = MultiPolygon(Polygon(tuple(ref_tuples)))
        kosm.point = kosm.mpoly.centroid
        kosm.lon, kosm.lat = kosm.point.tuple
    except:
        try:
            # add first point at the end to close the ring.
            tpl.append(tpl[0])
            kosm.mpoly = MultiPolygon(Polygon(tuple(ref_tuples)))
            kosm.point = kosm.mpoly.centroid
            kosm.lon, kosm.lat = kosm.point.tuple
        except:
            kosm.lon, kosm.lat = ref_tuples[0]
            kosm.set_geo()
    kosm.save()
    return True


def insert_refs_needed(refs):
    """ Insert alls refs needed to create the ways for polygon-based churches.
    """
    for ref_id in refs:
        try:
            ref, created = Ref.objects.get_or_create(osm_id=ref_id)
        except Ref.MultipleObjectsReturned:
            created = False
            ref = Ref.objects.filter(osm_id=ref_id)
            ref[1].delete()
            ref = ref[0]
        if not created:
            ref.need_update = True
        ref.save()
    return True


################################################################################

class GetChurches(object):
    """ collect all nodes and ways with amenity="place_of_worship"
    """

    def __init__(self, invalidate_refs=True):
        self.invalidate_refs = invalidate_refs


    def nodes(self, nodes):
        """ create for every place_of_worship node a task
        """
        for osmid, tags, refs in nodes:
            if 'amenity' in tags and tags.get('amenity') == 'place_of_worship':
                d = {'id': osmid, 'tags': tags, 'refs': refs}
                ## add task to celery
                insert_church_node.apply_async(args=[d])

    def ways(self, ways):
        """ create for every place_of_worship way a task
        """
        for osmid, tags, refs in ways:
            if 'amenity' in tags and tags.get('amenity') == 'place_of_worship':
                d = {'id': osmid, 'tags': tags, 'refs': refs}
                ## add refs needed for ways -- sync (wait for completion)
                if self.invalidate_refs:
                    insert_refs_needed(refs)
                ## add task to celery -- insert way / execute later (2h + x)
                insert_church_way.apply_async(args=[d],
                                              countdown=7200 +
                                              random.randint(1,3600),
                                              priority=8)


class GetRefs(object):
    """ Get all nodes for ways from first run.

    This class uses two methods to get all refs.
    If the length of the list is below 1000 it uses the full list.
    If the length of the list is longer than 1000 it iterates over the sorted
    list. This is important because in the openstreetmap planet we need to find
    over one million refs.
    """

    def __init__(self, threshold=1000):
        self.ref_id_list = Ref.objects.filter(
            need_update=True).order_by('osm_id').values_list('osm_id')
        self.use_full_list = False
        if len(self.ref_id_list) < threshold:
            self.use_full_list = True
            self.this_values = set(map(lambda x:x[0], self.ref_id_list))
        else:
            self.ref_list_len = len(self.ref_id_list)
            self.this_ref_index = 0
            self.this_value = self.get_value()

    def get_value(self):
        return self.ref_id_list[self.this_ref_index][0]

    def update_ref(self, osmid, lat, lon):
        try:
            ref_obj = Ref.objects.get(osm_id=osmid)
        except Ref.MultipleObjectsReturned:
            # if entry is a duplicate delete one of them.
            # they should be the same.
            ref_obj = Ref.objects.filter(osm_id=osmid)
            ref_obj[1].delete()
            ref_obj = ref_obj[0]

        ref_obj.set_point(lon, lat)
        ref_obj.need_update = False
        ref_obj.save()

    def coords(self, coords):
        """ save all coords to corresponding ref dataset
        """
        for osmid, lon, lat in coords:
            if self.use_full_list:
                if osmid in self.this_values:
                    self.update_ref(osmid, lat, lon)
                    self.this_values.remove(osmid)
            else:
                if osmid == self.this_value:
                    self.update_ref(osmid, lat, lon)
                if osmid >= self.this_value:
                    self.this_ref_index += 1
                    if self.this_ref_index >= self.ref_list_len:
                        break
                    self.this_value = self.get_value()

################################################################################

@task
def add_churches(filename, invalidate_refs=True):
    # get churches
    churches = GetChurches(invalidate_refs=invalidate_refs)
    p = OSMParser(concurrency=4,
                  nodes_callback=churches.nodes,
                  ways_callback=churches.ways)
    p.parse(filename)

    # don't run as task anymore:
#    update_refs(filename)
    return True


def update_refs(filename):
    # get refs
    missing_refs = Ref.objects.filter(need_update=True).count()
    while missing_refs>0:
        refs = GetRefs()
        p = OSMParser(concurrency=4,
                      coords_callback=refs.coords)
        p.parse(filename)

        missing_refs_neu = Ref.objects.filter(need_update=True).count()
        if missing_refs_neu == missing_refs:
            return False

    return True


def cleanup(num_of_days=None):
    """ delete all osm objects that are older than number_of_days.
    """

    if not num_of_days:
        raise ValueError, 'Please give number of days '
    'the church should be last updated'

    elements = KircheOsm.objects.filter(last_update__lt=(
            datetime.datetime.utcnow().replace(tzinfo=utc) -
            datetime.timedelta(days=num_of_days)))
    for elem in elements:
        elem.delete()
