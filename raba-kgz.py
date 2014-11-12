# coding: utf-8
'''
Translation functions for conversion of RABA-KGZ shp files into osm xml files

Usage:
ogr2osm$ python ./ogr2osm.py -t translations/raba-kgz.py ../raba-split/123/123.shp -o ../converted/123.osm

A translation functions for converting slovenian landuse to OpenStreetMap format
See https://wiki.openstreetmap.org/wiki/Slovenia_Landcover_Import_-_RABA-KGZ


The following fields are dropped from the source shapefile:

Field           Definition          Reason
AREA            Area size           Redundant, can be derived (calculated) from data
STATUS          ???                 No documentation


The following fields are used:    

Field           Used for            Reason
RABA_ID         landuse=*;natural=* Main tags
                raba:id             Serves as backup for easy mass change of mappings if needed, as some precision is lost in translation to OSM tags
RABA_PID        raba:pid            Unique ID for the area in the source
D_OD            raba:date           Date of last change in the source
VIR             raba:source         Source of data within the source

Polygon with RABA_ID=3000 (built-up areas) are skipped

Additional tags describing source:
source=RABA-KGZ
source:date=2014-09-11
'''


def filterFeature(ogrfeature, fieldNames, reproject):
    if ogrfeature is None:
        return

    index = ogrfeature.GetFieldIndex('RABA_ID')
    if index>0 and ogrfeature.GetField(index) == 3000:
        #print 'skipping' 
        #print ogrfeature.GetField(index)
        return None

    return ogrfeature

def filterTags(attrs):
    if not attrs:
        return
    tags = {}

    # tag source
    tags['source'] = 'RABA-KGZ'
    tags['source:date'] = '2014-09-11'

    # map RABA_ID to OSM tags
    if 'RABA_ID' in attrs:

        rabaid = attrs['RABA_ID'].strip()
        tags['raba:id'] = rabaid

        # NJIVE IN VRTOVI
        if rabaid == '1100': # Njiva (1000 m2)
            tags['landuse'] = 'farmland'
        elif rabaid == '1160': # Hmeljišče (500 m2)
            tags['landuse'] = 'farmland'
            tags['crop'] = 'hop'
        elif rabaid == '1180': # Trajne rastline na njivskih površinah (1000 m2)
            tags['landuse'] = 'plant_nursery'
        elif rabaid == '1190': # Rastlinjak (25 m2)
            tags['landuse'] = 'greenhouse_horticulture'

        # TRAJNI NASADI
        elif rabaid == '1211': # Vinograd (500 m2)
            tags['landuse'] = 'vineyard'
        elif rabaid == '1212': # Matičnjak (500 m2)
            tags['landuse'] = 'plant_nursery'
            tags['plant'] = 'vine'
        elif rabaid == '1221': # Intenzivni sadovnjak (1000 m2)
            tags['landuse'] = 'orchard'
        elif rabaid == '1222': # Ekstenzivni oziroma travniški sadovnjak (1000 m2)
            tags['landuse'] = 'orchard'
        elif rabaid == '1230': # Oljčnik (500 m2)
            tags['landuse'] = 'farmland'
            tags['trees'] = 'olive_trees'
        elif rabaid == '1240': # Ostali trajni nasadi (500 m2)
            tags['landuse'] = 'plantation'

        # TRAVNIŠKE POVRŠINE
        elif rabaid == '1300': # Trajni travnik (1000 m2)
            tags['landuse'] = 'meadow'
        elif rabaid == '1321': # Barjanski travnik (1000 m2)
            tags['natural'] = 'wetland'
            tags['wetland'] = 'marsh'
        elif rabaid == '1800': # Kmetijsko zemljišče, poraslo z gozdnim drevjem (1000 m2)
            tags['landuse'] = 'forest'

        # DRUGE KMETIJSKE POVRŠINE
        elif rabaid == '1410': # Kmetijsko zemljišče v zaraščanju (1000 m2)
            tags['natural'] = 'heath'
        elif rabaid == '1420': # Plantaža gozdnega drevja (1000 m2)
            tags['landuse'] = 'forest'
        elif rabaid == '1500': # Drevesa in grmičevje (1000 m2)
            tags['natural'] = 'scrub'
        elif rabaid == '1600': # Neobdelano kmetijsko zemljišče (1000 m2)
            tags['natural'] = 'scrub'

        # GOZD
        elif rabaid == '2000': # Gozd (2500m2)
            tags['landuse'] = 'forest'

        # OSTALA NEKMETIJSKA ZEMLJIŠČA
        elif rabaid == '3000': # Pozidano in sorodno zemljišče (25 m2)
            tags['landuse'] = 'construction'
            tags['fixme'] = 'should not be imported'
        elif rabaid == '4100': # Barje (5000 m2)
            tags['natural'] = 'wetland'
        elif rabaid == '4210': # Trstičje (5000 m2)
            tags['natural'] = 'wetland'
            tags['wetland'] = 'reedbed'
        elif rabaid == '4220': # Ostalo zamočvirjeno zemljišče (5000 m2)
            tags['natural'] = 'wetland'
        elif rabaid == '5000': # Suho, odprto zemljišče s posebnim rastlinskim pokrovom (5000 m2)
            tags['natural'] = 'moor'
        elif rabaid == '6000': # Odprto zemljišče brez ali z nepomembnim rastlinskim pokrovom (5000 m2)
            tags['natural'] = 'bare_rock'
        elif rabaid == '7000': # Voda (25 m2)
            tags['natural'] = 'water'

        else:
            tags['fixme'] = 'unknown raba_id: ' + rabaid
            

    if 'RABA_PID' in attrs:
        tags['raba:pid'] = attrs['RABA_PID'].strip()

    if 'D_OD' in attrs:
        tags['raba:date'] = attrs['D_OD'].strip()

    if 'VIR' in attrs:
        tags['raba:source'] = attrs['VIR'].strip()

    return tags