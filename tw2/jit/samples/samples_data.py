# This module just contains some of the more lengthy constants used in
# samples.py that would otherwise clutter that file.
from random import randint, random
BarChartJSONSampleData = {
    'label': ['label A', 'label B', 'label C', 'label D'],
    'values': [
        {
            'label': 'date A',
            'values': [20, 40, 15, 5]
        },
        {
            'label': 'date B',
            'values': [30, 10, 45, 10]
        },
        {
            'label': 'date E',
            'values': [38, 20, 35, 17]
        },
        {
            'label': 'date F',
            'values': [58, 10, 35, 32]
        },
        {
            'label': 'date D',
            'values': [55, 60, 34, 38]
        },
        {
            'label': 'date C',
            'values': [26, 40, 25, 40],
        }
    ]
}

AreaChartJSONSampleData = {
    'label' : ['Top income of the lowest quintile (%20) in the US',
               'Top income of the second quintile',
               'Top income of the third quintile',
               'Top income of the fourth quintile',
               'Bottom of top %5'],
    'values' : [entry for entry in reversed([
        {
            'label': '09',
            'values': [20453,38550,61801,100000,180001]
        }, {
            'label': '08',
            'values': [20633,38852,62487,99860,179317]
        }, {
            'label': '07',
            'values': [20991,40448,64138,103448,183103]
        }, {
            'label': '06',
            'values': [21314,40185,63830,103226,185119]
        }, {
            'label': '05',
            'values': [21071,39554,63352,100757,182386]
        }, {
            'label': '04',
            'values': [20992,39375,62716,99930,178453]
        }, {
            'label': '03',
            'values': [20974,39652,63505,101307,179740]
        }, {
            'label': '02',
            'values': [21361,39795,63384,100170,178844]
        }, {
            'label': '01',
            'values': [21771,40361,64212,101163,182335]
        }, {
            'label': '00',
            'values': [22320,41103,64985,101844,180879]
        }, {
            'label': '99',
            'values': [22059,41090,64859,101995,182795]
        }, {
            'label': '98',
            'values': [21179,39960,63522,98561,173728]
        }, {
            'label': '97',
            'values': [20520,38909,61294,95273,168626]
        }, {
            'label': '96',
            'values': [20103,37789,59904,92587,162727]
        }, {
            'label': '95',
            'values': [20124,37613,58698,91012,157919]
        }, {
            'label': '94',
            'values': [19215,36065,57390,89936,157172]
        }, {
            'label': '93',
            'values': [18954,36074,56704,88142,152953]
        }, {
            'label': '92',
            'values': [18873,36158,56769,86886,148318]
        }, {
            'label': '91',
            'values': [19338,36860,56933,87173,148055]
        }, {
            'label': '90',
            'values': [19886,37644,57591,87826,150735]
        }, {
            'label': '89',
            'values': [20203,38415,59042,89707,153241]
        }, {
            'label': '88',
            'values': [19830,37459,58376,88146,149207]
        }, {
            'label': '87',
            'values': [19507,37027,57798,87353,146172]
        }, {
            'label': '86',
            'values': [19133,36598,56799,85859,143974]
        }, {
            'label': '85',
            'values': [18898,35557,55082,82843,136881]
        }, {
            'label': '84',
            'values': [18680,34961,53863,81365,134691]
        }, {
            'label': '83',
            'values': [18317,34058,52273,78998,129971]
        }, {
            'label': '82',
            'values': [17927,34095,52095,77683,128232]
        }, {
            'label': '81',
            'values': [18158,33944,52500,77619,124914]
        }, {
            'label': '80',
            'values': [18533,34757,53285,78019,125556]
        }, {
            'label': '79',
            'values': [19274,35795,55073,79851,129029]
        }, {
            'label': '78',
            'values': [19063,36044,54537,79317,126890]
        }, {
            'label': '77',
            'values': [18487,34821,53076,77380,122518]
        }, {
            'label': '76',
            'values': [18526,34516,52580,75648,119967]
        }, {
            'label': '75',
            'values': [18124,34016,51400,73802,116463]
        }, {
            'label': '74',
            'values': [19065,35364,52255,75839,120037]
        }, {
            'label': '73',
            'values': [18973,36484,53982,77723,124921]
        }, {
            'label': '72',
            'values': [18570,35764,52858,75655,121759]
        }, {
            'label': '71',
            'values': [17946,34211,50343,71784,113995]
        }, {
            'label': '70',
            'values': [18180,34827,50656,72273,114243]
        }, {
            'label': '69',
            'values': [18491,35483,51316,71897,112759]
        }, {
            'label': '68',
            'values': [17954,34039,48790,68554,107251]
        }, {
            'label': '67',
            'values': [16845,32848,46621,66481,106684]
        }
    ])]
}

def icicleColor(level, total, val):
    magic = 0.49 # lol
    total = total + 1
    coeff = magic/total
    perturb = coeff*val/10.0
    base = (level+magic)/total + perturb
    assert(base >= 0 and base <= 1)
    R = int(256*base)
    G = int(128*base)
    B = int(256*(1 - base))
    return "#" + "".join(
        ["%2s" % hex(component)[2:] for component in [R, G, B]]
    ).replace(' ', '0')

def generateTree(total_levels=2, _level=0, _index=0, pid='', code=''):
    val = randint(1,10)
    id = '%i_%i_%s' % (_level, _index, pid)
    this_node = {
        'id' : "%s_inode_%s" % (code, id),
        'name' : "%i" % val,
        'data' : {
            '$area' : val,
            '$dim' : val,
            '$color' : icicleColor(_level, total_levels, val)
        }
    }
    if _level < total_levels:
        this_node['children'] = [
            generateTree(total_levels, _level+1, i, id, code)
                for i in range(randint(2,4))
        ]
    return this_node


IcicleJSONSampleData = generateTree(5, code='icicle')
SpaceTreeJSONSampleData = generateTree(3, code='spacetree')

PieChartJSONSampleData = BarChartJSONSampleData
TreeMapJSONSampleData = {
  "children": [
   {
     "children": [
       {
         "children": [],
         "data": {
           "playcount": "276",
           "$color": "#8E7032",
           "image": "http://userserve-ak.last.fm/serve/300x300/11403219.jpg",
           "$area": 276
         },
         "id": "album-Thirteenth Step",
         "name": "Thirteenth Step"
       },
       {
         "children": [],
         "data": {
           "playcount": "271",
           "$color": "#906E32",
           "image": "http://userserve-ak.last.fm/serve/300x300/11393921.jpg",
           "$area": 271
         },
         "id": "album-Mer De Noms",
         "name": "Mer De Noms"
       }
     ],
     "data": {
       "playcount": 547,
       "$area": 547
     },
     "id": "artist_A Perfect Circle",
     "name": "A Perfect Circle"
   },
   {
     "children": [
       {
         "children": [],
         "data": {
           "playcount": "209",
           "$color": "#AA5532",
           "image": "http://userserve-ak.last.fm/serve/300x300/32349839.jpg",
           "$area": 209
         },
         "id": "album-Above",
         "name": "Above"
       }
     ],
     "data": {
       "playcount": 209,
       "$area": 209
     },
     "id": "artist_Mad Season",
     "name": "Mad Season"
   },
   {
     "children": [
       {
         "children": [],
         "data": {
           "playcount": "260",
           "$color": "#956932",
           "image": "http://userserve-ak.last.fm/serve/300x300/38753425.jpg",
           "$area": 260
         },
         "id": "album-Tiny Music... Songs From the Vatican Gift Shop",
         "name": "Tiny Music... Songs From the Vatican Gift Shop"
       },
       {
         "children": [],
         "data": {
           "playcount": "254",
           "$color": "#976732",
           "image": "http://images.amazon.com/images/P/B000002IU3.01.LZZZZZZZ.jpg",
           "$area": 254
         },
         "id": "album-Core",
         "name": "Core"
       }
     ],
     "data": {
       "playcount": 514,
       "$area": 514
     },
     "id": "artist_Stone Temple Pilots",
     "name": "Stone Temple Pilots"
   },
   {
     "children": [
       {
         "children": [],
         "data": {
           "playcount": "181",
           "$color": "#B54932",
           "image": "http://userserve-ak.last.fm/serve/300x300/8673371.jpg",
           "$area": 181
         },
         "id": "album-The Science of Things",
         "name": "The Science of Things"
       }
     ],
     "data": {
       "playcount": 181,
       "$area": 181
     },
     "id": "artist_Bush",
     "name": "Bush"
   },
   {
     "children": [
       {
         "children": [],
         "data": {
           "playcount": "229",
           "$color": "#A15D32",
           "image": "http://userserve-ak.last.fm/serve/300x300/32579429.jpg",
           "$area": 229
         },
         "id": "album-Echoes, Silence, Patience &amp; Grace",
         "name": "Echoes, Silence, Patience &amp; Grace"
       },
       {
         "children": [],
         "data": {
           "playcount": "185",
           "$color": "#B34B32",
           "image": "http://images.amazon.com/images/P/B0009HLDFU.01.MZZZZZZZ.jpg",
           "$area": 185
         },
         "id": "album-In Your Honor (disc 2)",
         "name": "In Your Honor (disc 2)"
       }
     ],
     "data": {
       "playcount": 414,
       "$area": 414
     },
     "id": "artist_Foo Fighters",
     "name": "Foo Fighters"
   },
   {
     "children": [
       {
         "children": [],
         "data": {
           "playcount": "398",
           "$color": "#5DA132",
           "image": "http://images.amazon.com/images/P/B00005LNP5.01._SCMZZZZZZZ_.jpg",
           "$area": 398
         },
         "id": "album-Elija Y Gane",
         "name": "Elija Y Gane"
       },
       {
         "children": [],
         "data": {
           "playcount": "203",
           "$color": "#AC5232",
           "image": "http://images.amazon.com/images/P/B0000B193V.01._SCMZZZZZZZ_.jpg",
           "$area": 203
         },
         "id": "album-Para los Arboles",
         "name": "Para los Arboles"
       }
     ],
     "data": {
       "playcount": 601,
       "$area": 601
     },
     "id": "artist_Luis Alberto Spinetta",
     "name": "Luis Alberto Spinetta"
   },
   {
     "children": [
       {
         "children": [],
         "data": {
           "playcount": "224",
           "$color": "#A35B32",
           "image": "http://userserve-ak.last.fm/serve/300x300/26497553.jpg",
           "$area": 224
         },
         "id": "album-Music Bank",
         "name": "Music Bank"
       },
       {
         "children": [],
         "data": {
           "playcount": "217",
           "$color": "#A65832",
           "image": "http://images.amazon.com/images/P/B0000296JW.01.MZZZZZZZ.jpg",
           "$area": 217
         },
         "id": "album-Music Bank (disc 1)",
         "name": "Music Bank (disc 1)"
       },
       {
         "children": [],
         "data": {
           "playcount": "215",
           "$color": "#A75732",
           "image": "http://images.amazon.com/images/P/B0000296JW.01.MZZZZZZZ.jpg",
           "$area": 215
         },
         "id": "album-Music Bank (disc 2)",
         "name": "Music Bank (disc 2)"
       },
       {
         "children": [],
         "data": {
           "playcount": "181",
           "$color": "#B54932",
           "image": "http://images.amazon.com/images/P/B0000296JW.01.MZZZZZZZ.jpg",
           "$area": 181
         },
         "id": "album-Music Bank (disc 3)",
         "name": "Music Bank (disc 3)"
       }
     ],
     "data": {
       "playcount": 837,
       "$area": 837
     },
     "id": "artist_Alice in Chains",
     "name": "Alice in Chains"
   },
   {
     "children": [
       {
         "children": [],
         "data": {
           "playcount": "627",
           "$color": "#00FF32",
           "image": "http://userserve-ak.last.fm/serve/300x300/8480501.jpg",
           "$area": 627
         },
         "id": "album-10,000 Days",
         "name": "10,000 Days"
       }
     ],
     "data": {
       "playcount": 627,
       "$area": 627
     },
     "id": "artist_Tool",
     "name": "Tool"
   },
   {
     "children": [
       {
         "children": [],
         "data": {
           "playcount": "261",
           "$color": "#946A32",
           "image": "http://cdn.last.fm/flatness/catalogue/noimage/2/default_album_medium.png",
           "$area": 261
         },
         "id": "album-2006-09-07: O-Bar, Stockholm, Sweden",
         "name": "2006-09-07: O-Bar, Stockholm, Sweden"
       },
       {
         "children": [],
         "data": {
           "playcount": "211",
           "$color": "#A95532",
           "image": "http://userserve-ak.last.fm/serve/300x300/25402479.jpg",
           "$area": 211
         },
         "id": "album-Lost and Found",
         "name": "Lost and Found"
       }
     ],
     "data": {
       "playcount": 472,
       "$area": 472
     },
     "id": "artist_Chris Cornell",
     "name": "Chris Cornell"
   },
   {
     "children": [
       {
         "children": [],
         "data": {
           "playcount": "197",
           "$color": "#AE5032",
           "image": "http://userserve-ak.last.fm/serve/300x300/8634627.jpg",
           "$area": 197
         },
         "id": "album-The Sickness",
         "name": "The Sickness"
       }
     ],
     "data": {
       "playcount": 197,
       "$area": 197
     },
     "id": "artist_Disturbed",
     "name": "Disturbed"
   },
   {
     "children": [
       {
         "children": [],
         "data": {
           "playcount": "493",
           "$color": "#36C832",
           "image": "http://userserve-ak.last.fm/serve/300x300/8591345.jpg",
           "$area": 493
         },
         "id": "album-Mama's Gun",
         "name": "Mama's Gun"
       }
     ],
     "data": {
       "playcount": 493,
       "$area": 493
     },
     "id": "artist_Erykah Badu",
     "name": "Erykah Badu"
   },
   {
     "children": [
       {
         "children": [],
         "data": {
           "playcount": "249",
           "$color": "#996532",
           "image": "http://userserve-ak.last.fm/serve/300x300/32070871.jpg",
           "$area": 249
         },
         "id": "album-Audioslave",
         "name": "Audioslave"
       }
     ],
     "data": {
       "playcount": 249,
       "$area": 249
     },
     "id": "artist_Audioslave",
     "name": "Audioslave"
   },
   {
     "children": [
       {
         "children": [],
         "data": {
           "playcount": "359",
           "$color": "#6C9232",
           "image": "http://userserve-ak.last.fm/serve/300x300/15858421.jpg",
           "$area": 359
         },
         "id": "album-Comfort y M\u00fasica Para Volar",
         "name": "Comfort y M\u00fasica Para Volar"
       }
     ],
     "data": {
       "playcount": 359,
       "$area": 359
     },
     "id": "artist_Soda Stereo",
     "name": "Soda Stereo"
   },
   {
     "children": [
       {
         "children": [],
         "data": {
           "playcount": "302",
           "$color": "#847A32",
           "image": "http://userserve-ak.last.fm/serve/300x300/8776205.jpg",
           "$area": 302
         },
         "id": "album-Clearing the Channel",
         "name": "Clearing the Channel"
       }
     ],
     "data": {
       "playcount": 302,
       "$area": 302
     },
     "id": "artist_Sinch",
     "name": "Sinch"
   },
   {
     "children": [
       {
         "children": [],
         "data": {
           "playcount": "177",
           "$color": "#B74732",
           "image": "http://userserve-ak.last.fm/serve/300x300/32457599.jpg",
           "$area": 177
         },
         "id": "album-Crash",
         "name": "Crash"
       }
     ],
     "data": {
       "playcount": 177,
       "$area": 177
     },
     "id": "artist_Dave Matthews Band",
     "name": "Dave Matthews Band"
   },
   {
     "children": [
       {
         "children": [],
         "data": {
           "playcount": "207",
           "$color": "#AA5432",
           "image": "http://userserve-ak.last.fm/serve/300x300/30352203.jpg",
           "$area": 207
         },
         "id": "album-Vs.",
         "name": "Vs."
       }
     ],
     "data": {
       "playcount": 207,
       "$area": 207
     },
     "id": "artist_Pearl Jam",
     "name": "Pearl Jam"
   },
   {
     "children": [
       {
         "children": [],
         "data": {
           "playcount": "486",
           "$color": "#39C532",
           "image": "http://userserve-ak.last.fm/serve/300x300/26053425.jpg",
           "$area": 486
         },
         "id": "album-It All Makes Sense Now",
         "name": "It All Makes Sense Now"
       },
       {
         "children": [],
         "data": {
           "playcount": "251",
           "$color": "#986632",
           "image": "http://userserve-ak.last.fm/serve/300x300/9658733.jpg",
           "$area": 251
         },
         "id": "album-Air",
         "name": "Air"
       }
     ],
     "data": {
       "playcount": 737,
       "$area": 737
     },
     "id": "artist_Kr\u00f8m",
     "name": "Kr\u00f8m"
   },
   {
     "children": [
       {
         "children": [],
         "data": {
           "playcount": "345",
           "$color": "#728C32",
           "image": "http://userserve-ak.last.fm/serve/300x300/8605651.jpg",
           "$area": 345
         },
         "id": "album-Temple Of The Dog",
         "name": "Temple Of The Dog"
       }
     ],
     "data": {
       "playcount": 345,
       "$area": 345
     },
     "id": "artist_Temple of the Dog",
     "name": "Temple of the Dog"
   },
   {
     "children": [
       {
         "children": [],
         "data": {
           "playcount": "318",
           "$color": "#7D8132",
           "image": "http://userserve-ak.last.fm/serve/300x300/29274729.jpg",
           "$area": 318
         },
         "id": "album-And All That Could Have Been (Still)",
         "name": "And All That Could Have Been (Still)"
       }
     ],
     "data": {
       "playcount": 318,
       "$area": 318
     },
     "id": "artist_Nine Inch Nails",
     "name": "Nine Inch Nails"
   },
   {
     "children": [
       {
         "children": [],
         "data": {
           "playcount": "256",
           "$color": "#966832",
           "image": "http://userserve-ak.last.fm/serve/300x300/32595059.jpg",
           "$area": 256
         },
         "id": "album-Mamagubida",
         "name": "Mamagubida"
       },
       {
         "children": [],
         "data": {
           "playcount": "220",
           "$color": "#A55932",
           "image": "http://cdn.last.fm/flatness/catalogue/noimage/2/default_album_medium.png",
           "$area": 220
         },
         "id": "album-Reggae \u00e0 Coup de Cirque",
         "name": "Reggae \u00e0 Coup de Cirque"
       },
       {
         "children": [],
         "data": {
           "playcount": "181",
           "$color": "#B54932",
           "image": "http://userserve-ak.last.fm/serve/300x300/16799743.jpg",
           "$area": 181
         },
         "id": "album-Grain de sable",
         "name": "Grain de sable"
       }
     ],
     "data": {
       "playcount": 657,
       "$area": 657
     },
     "id": "artist_Tryo",
     "name": "Tryo"
   },
   {
     "children": [
       {
         "children": [],
         "data": {
           "playcount": "258",
           "$color": "#966832",
           "image": "http://cdn.last.fm/flatness/catalogue/noimage/2/default_album_medium.png",
           "$area": 258
         },
         "id": "album-Best Of",
         "name": "Best Of"
       },
       {
         "children": [],
         "data": {
           "playcount": "176",
           "$color": "#B74732",
           "image": "http://userserve-ak.last.fm/serve/300x300/5264426.jpg",
           "$area": 176
         },
         "id": "album-Robbin' The Hood",
         "name": "Robbin' The Hood"
       }
     ],
     "data": {
       "playcount": 434,
       "$area": 434
     },
     "id": "artist_Sublime",
     "name": "Sublime"
   },
   {
     "children": [
       {
         "children": [],
         "data": {
           "playcount": "418",
           "$color": "#55AA32",
           "image": "http://userserve-ak.last.fm/serve/300x300/8590493.jpg",
           "$area": 418
         },
         "id": "album-One Hot Minute",
         "name": "One Hot Minute"
       }
     ],
     "data": {
       "playcount": 418,
       "$area": 418
     },
     "id": "artist_Red Hot Chili Peppers",
     "name": "Red Hot Chili Peppers"
   },
   {
     "children": [
       {
         "children": [],
         "data": {
           "playcount": "275",
           "$color": "#8F6F32",
           "image": "http://userserve-ak.last.fm/serve/300x300/17597653.jpg",
           "$area": 275
         },
         "id": "album-Chinese Democracy",
         "name": "Chinese Democracy"
       },
       {
         "children": [],
         "data": {
           "playcount": "203",
           "$color": "#AC5232",
           "image": "http://userserve-ak.last.fm/serve/300x300/15231979.jpg",
           "$area": 203
         },
         "id": "album-Use Your Illusion II",
         "name": "Use Your Illusion II"
       }
     ],
     "data": {
       "playcount": 478,
       "$area": 478
     },
     "id": "artist_Guns N' Roses",
     "name": "Guns N' Roses"
   },
   {
     "children": [
       {
         "children": [],
         "data": {
           "playcount": "208",
           "$color": "#AA5432",
           "image": "http://images.amazon.com/images/P/B0007LCNNE.01.MZZZZZZZ.jpg",
           "$area": 208
         },
         "id": "album-Tales of the Forgotten Melodies",
         "name": "Tales of the Forgotten Melodies"
       }
     ],
     "data": {
       "playcount": 208,
       "$area": 208
     },
     "id": "artist_Wax Tailor",
     "name": "Wax Tailor"
   },
   {
     "children": [
       {
         "children": [],
         "data": {
           "playcount": "208",
           "$color": "#AA5432",
           "image": "http://userserve-ak.last.fm/serve/300x300/7862623.png",
           "$area": 208
         },
         "id": "album-In Rainbows",
         "name": "In Rainbows"
       }
     ],
     "data": {
       "playcount": 208,
       "$area": 208
     },
     "id": "artist_Radiohead",
     "name": "Radiohead"
   },
   {
     "children": [
       {
         "children": [],
         "data": {
           "playcount": "317",
           "$color": "#7E8032",
           "image": "http://userserve-ak.last.fm/serve/300x300/8600371.jpg",
           "$area": 317
         },
         "id": "album-Down On The Upside",
         "name": "Down On The Upside"
       },
       {
         "children": [],
         "data": {
           "playcount": "290",
           "$color": "#897532",
           "image": "http://userserve-ak.last.fm/serve/300x300/8590515.jpg",
           "$area": 290
         },
         "id": "album-Superunknown",
         "name": "Superunknown"
       }
     ],
     "data": {
       "playcount": 607,
       "$area": 607
     },
     "id": "artist_Soundgarden",
     "name": "Soundgarden"
   },
   {
     "children": [
       {
         "children": [],
         "data": {
           "playcount": "247",
           "$color": "#9A6432",
           "image": "http://userserve-ak.last.fm/serve/300x300/15113951.jpg",
           "$area": 247
         },
         "id": "album-Nico",
         "name": "Nico"
       },
       {
         "children": [],
         "data": {
           "playcount": "218",
           "$color": "#A65832",
           "image": "http://userserve-ak.last.fm/serve/300x300/45729417.jpg",
           "$area": 218
         },
         "id": "album-Soup",
         "name": "Soup"
       },
       {
         "children": [],
         "data": {
           "playcount": "197",
           "$color": "#AE5032",
           "image": "http://images.amazon.com/images/P/B00005V5PW.01.MZZZZZZZ.jpg",
           "$area": 197
         },
         "id": "album-Classic Masters",
         "name": "Classic Masters"
       },
       {
         "children": [],
         "data": {
           "playcount": "194",
           "$color": "#B04E32",
           "image": "http://userserve-ak.last.fm/serve/300x300/15157989.jpg",
           "$area": 194
         },
         "id": "album-Blind Melon",
         "name": "Blind Melon"
       }
     ],
     "data": {
       "playcount": 856,
       "$area": 856
     },
     "id": "artist_Blind Melon",
     "name": "Blind Melon"
   },
   {
     "children": [
       {
         "children": [],
         "data": {
           "playcount": "537",
           "$color": "#24DA32",
           "image": "http://userserve-ak.last.fm/serve/300x300/17594883.jpg",
           "$area": 537
         },
         "id": "album-Make Yourself",
         "name": "Make Yourself"
       },
       {
         "children": [],
         "data": {
           "playcount": "258",
           "$color": "#966832",
           "image": "http://userserve-ak.last.fm/serve/300x300/31550385.jpg",
           "$area": 258
         },
         "id": "album-Light Grenades",
         "name": "Light Grenades"
       },
       {
         "children": [],
         "data": {
           "playcount": "181",
           "$color": "#B54932",
           "image": "http://userserve-ak.last.fm/serve/300x300/32309285.jpg",
           "$area": 181
         },
         "id": "album-Morning View",
         "name": "Morning View"
       }
     ],
     "data": {
       "playcount": 976,
       "$area": 976
     },
     "id": "artist_Incubus",
     "name": "Incubus"
   },
   {
     "children": [
       {
         "children": [],
         "data": {
           "playcount": "198",
           "$color": "#AE5032",
           "image": "http://userserve-ak.last.fm/serve/300x300/8599099.jpg",
           "$area": 198
         },
         "id": "album-On And On",
         "name": "On And On"
       },
       {
         "children": [],
         "data": {
           "playcount": "186",
           "$color": "#B34B32",
           "image": "http://userserve-ak.last.fm/serve/300x300/30082075.jpg",
           "$area": 186
         },
         "id": "album-Brushfire Fairytales",
         "name": "Brushfire Fairytales"
       }
     ],
     "data": {
       "playcount": 384,
       "$area": 384
     },
     "id": "artist_Jack Johnson",
     "name": "Jack Johnson"
   },
   {
     "children": [
       {
         "children": [],
         "data": {
           "playcount": "349",
           "$color": "#718D32",
           "image": "http://userserve-ak.last.fm/serve/300x300/21881921.jpg",
           "$area": 349
         },
         "id": "album-Mother Love Bone",
         "name": "Mother Love Bone"
       }
     ],
     "data": {
       "playcount": 349,
       "$area": 349
     },
     "id": "artist_Mother Love Bone",
     "name": "Mother Love Bone"
   }
 ],
 "data": {},
 "id": "root",
 "name": "Top Albums"
}

ForceDirectedGraphJSONSampleData = [
{
        "adjacencies": [
            "graphnode21",
            {
              "nodeTo": "graphnode1",
              "nodeFrom": "graphnode0",
              "data": {
                "$color": "#557EAA"
              }
            }, {
              "nodeTo": "graphnode13",
              "nodeFrom": "graphnode0",
              "data": {
                "$color": "#909291"
              }
            }, {
              "nodeTo": "graphnode14",
              "nodeFrom": "graphnode0",
              "data": {
                "$color": "#557EAA"
              }
            }, {
              "nodeTo": "graphnode15",
              "nodeFrom": "graphnode0",
              "data": {
                "$color": "#557EAA"
              }
            }, {
              "nodeTo": "graphnode16",
              "nodeFrom": "graphnode0",
              "data": {
                "$color": "#557EAA"
              }
            }, {
              "nodeTo": "graphnode17",
              "nodeFrom": "graphnode0",
              "data": {
                "$color": "#557EAA"
              }
            }
        ],
        "data": {
          "$color": "#83548B",
          "$type": "circle",
          "$dim": 10
        },
        "id": "graphnode0",
        "name": "graphnode0"
      }, {
        "adjacencies": [
            {
              "nodeTo": "graphnode2",
              "nodeFrom": "graphnode1",
              "data": {
                "$color": "#557EAA"
              }
            }, {
              "nodeTo": "graphnode4",
              "nodeFrom": "graphnode1",
              "data": {
                "$color": "#909291"
              }
            }, {
              "nodeTo": "graphnode5",
              "nodeFrom": "graphnode1",
              "data": {
                "$color": "#909291"
              }
            }, {
              "nodeTo": "graphnode6",
              "nodeFrom": "graphnode1",
              "data": {
                "$color": "#909291"
              }
            }, {
              "nodeTo": "graphnode7",
              "nodeFrom": "graphnode1",
              "data": {
                "$color": "#909291"
              }
            }, {
              "nodeTo": "graphnode8",
              "nodeFrom": "graphnode1",
              "data": {
                "$color": "#909291"
              }
            }, {
              "nodeTo": "graphnode10",
              "nodeFrom": "graphnode1",
              "data": {
                "$color": "#557EAA"
              }
            }, {
              "nodeTo": "graphnode11",
              "nodeFrom": "graphnode1",
              "data": {
                "$color": "#909291"
              }
            }, {
              "nodeTo": "graphnode12",
              "nodeFrom": "graphnode1",
              "data": {
                "$color": "#909291"
              }
            }, {
              "nodeTo": "graphnode13",
              "nodeFrom": "graphnode1",
              "data": {
                "$color": "#557EAA"
              }
            }, {
              "nodeTo": "graphnode14",
              "nodeFrom": "graphnode1",
              "data": {
                "$color": "#557EAA"
              }
            }, {
              "nodeTo": "graphnode15",
              "nodeFrom": "graphnode1",
              "data": {
                "$color": "#557EAA"
              }
            }, {
              "nodeTo": "graphnode16",
              "nodeFrom": "graphnode1",
              "data": {
                "$color": "#909291"
              }
            }, {
              "nodeTo": "graphnode17",
              "nodeFrom": "graphnode1",
              "data": {
                "$color": "#557EAA"
              }
            }
        ],
        "data": {
          "$color": "#EBB056",
          "$type": "circle",
          "$dim": 11
        },
        "id": "graphnode1",
        "name": "graphnode1"
      }, {
        "adjacencies": [
            {
              "nodeTo": "graphnode5",
              "nodeFrom": "graphnode2",
              "data": {
                "$color": "#909291"
              }
            }, {
              "nodeTo": "graphnode9",
              "nodeFrom": "graphnode2",
              "data": {
                "$color": "#557EAA"
              }
            }, {
              "nodeTo": "graphnode18",
              "nodeFrom": "graphnode2",
              "data": {
                "$color": "#557EAA"
              }
            }
        ],
        "data": {
          "$color": "#416D9C",
          "$type": "circle",
          "$dim": 7
        },
        "id": "graphnode2",
        "name": "graphnode2"
      }, {
        "adjacencies": [
            {
              "nodeTo": "graphnode5",
              "nodeFrom": "graphnode3",
              "data": {
                "$color": "#909291"
              }
            }, {
              "nodeTo": "graphnode9",
              "nodeFrom": "graphnode3",
              "data": {
                "$color": "#557EAA"
              }
            }, {
              "nodeTo": "graphnode10",
              "nodeFrom": "graphnode3",
              "data": {
                "$color": "#557EAA"
              }
            }, {
              "nodeTo": "graphnode12",
              "nodeFrom": "graphnode3",
              "data": {
                "$color": "#557EAA"
              }
            }
        ],
        "data": {
          "$color": "#416D9C",
          "$type": "square",
          "$dim": 10
        },
        "id": "graphnode3",
        "name": "graphnode3"
      }, {
        "adjacencies": [],
        "data": {
          "$color": "#83548B",
          "$type": "square",
          "$dim": 11
        },
        "id": "graphnode4",
        "name": "graphnode4"
      }, {
        "adjacencies": [
          {
            "nodeTo": "graphnode9",
            "nodeFrom": "graphnode5",
            "data": {
              "$color": "#909291"
            }
          }
        ],
        "data": {
          "$color": "#C74243",
          "$type": "triangle",
          "$dim": 8
        },
        "id": "graphnode5",
        "name": "graphnode5"
      }, {
        "adjacencies": [
            {
              "nodeTo": "graphnode10",
              "nodeFrom": "graphnode6",
              "data": {
                "$color": "#557EAA"
              }
            }, {
              "nodeTo": "graphnode11",
              "nodeFrom": "graphnode6",
              "data": {
                "$color": "#557EAA"
              }
            }
        ],
        "data": {
          "$color": "#83548B",
          "$type": "circle",
          "$dim": 11
        },
        "id": "graphnode6",
        "name": "graphnode6"
      }, {
        "adjacencies": [],
        "data": {
          "$color": "#EBB056",
          "$type": "triangle",
          "$dim": 12
        },
        "id": "graphnode7",
        "name": "graphnode7"
      }, {
        "adjacencies": [],
        "data": {
          "$color": "#C74243",
          "$type": "star",
          "$dim": 10
        },
        "id": "graphnode8",
        "name": "graphnode8"
      }, {
        "adjacencies": [],
        "data": {
          "$color": "#83548B",
          "$type": "circle",
          "$dim": 12
        },
        "id": "graphnode9",
        "name": "graphnode9"
      }, {
        "adjacencies": [
          {
            "nodeTo": "graphnode11",
            "nodeFrom": "graphnode10",
            "data": {
              "$color": "#909291"
            }
          }
        ],
        "data": {
          "$color": "#70A35E",
          "$type": "triangle",
          "$dim": 11
        },
        "id": "graphnode10",
        "name": "graphnode10"
      }, {
        "adjacencies": [],
        "data": {
          "$color": "#70A35E",
          "$type": "circle",
          "$dim": 11
        },
        "id": "graphnode11",
        "name": "graphnode11"
      }, {
        "adjacencies": [],
        "data": {
          "$color": "#83548B",
          "$type": "triangle",
          "$dim": 10
        },
        "id": "graphnode12",
        "name": "graphnode12"
      }, {
        "adjacencies": [
          {
            "nodeTo": "graphnode14",
            "nodeFrom": "graphnode13",
            "data": {
              "$color": "#557EAA"
            }
          }
        ],
        "data": {
          "$color": "#EBB056",
          "$type": "star",
          "$dim": 7
        },
        "id": "graphnode13",
        "name": "graphnode13"
      }, {
        "adjacencies": [],
        "data": {
          "$color": "#EBB056",
          "$type": "triangle",
          "$dim": 12
        },
        "id": "graphnode14",
        "name": "graphnode14"
      }, {
        "adjacencies": [
            {
              "nodeTo": "graphnode16",
              "nodeFrom": "graphnode15",
              "data": {
                "$color": "#557EAA"
              }
            }, {
              "nodeTo": "graphnode17",
              "nodeFrom": "graphnode15",
              "data": {
                "$color": "#557EAA"
              }
            }
        ],
        "data": {
          "$color": "#83548B",
          "$type": "triangle",
          "$dim": 11
        },
        "id": "graphnode15",
        "name": "graphnode15"
      }, {
        "adjacencies": [
          {
            "nodeTo": "graphnode17",
            "nodeFrom": "graphnode16",
            "data": {
              "$color": "#557EAA"
            }
          }
        ],
        "data": {
          "$color": "#C74243",
          "$type": "star",
          "$dim": 7
        },
        "id": "graphnode16",
        "name": "graphnode16"
      }, {
        "adjacencies": [],
        "data": {
          "$color": "#416D9C",
          "$type": "circle",
          "$dim": 7
        },
        "id": "graphnode17",
        "name": "graphnode17"
      }, {
        "adjacencies": [
            {
              "nodeTo": "graphnode19",
              "nodeFrom": "graphnode18",
              "data": {
                "$color": "#557EAA"
              }
            }, {
              "nodeTo": "graphnode20",
              "nodeFrom": "graphnode18",
              "data": {
                "$color": "#557EAA"
              }
            }
        ],
        "data": {
          "$color": "#EBB056",
          "$type": "triangle",
          "$dim": 9
        },
        "id": "graphnode18",
        "name": "graphnode18"
      }, {
        "adjacencies": [],
        "data": {
          "$color": "#70A35E",
          "$type": "circle",
          "$dim": 8
        },
        "id": "graphnode19",
        "name": "graphnode19"
      }, {
        "adjacencies": [],
        "data": {
          "$color": "#C74243",
          "$type": "star",
          "$dim": 8
        },
        "id": "graphnode20",
        "name": "graphnode20"
      }
]

RadialGraphJSONSampleData = {
"id": "190_0",
    "name": "Pearl Jamx0r",
    "children": [{
        "id": "306208_1",
        "name": "Pearl Jam &amp; Cypress Hill",
        "data": {
            "relation": "<h4>Pearl Jam &amp; Cypress Hill</h4><b>Connections:</b><ul><li>Pearl Jam <div>(relation: collaboration)</div></li><li>Cypress Hill <div>(relation: collaboration)</div></li></ul>"
        },
        "children": [{
            "id": "84_2",
            "name": "Cypress Hill",
            "data": {
                "relation": "<h4>Cypress Hill</h4><b>Connections:</b><ul><li>Pearl Jam &amp; Cypress Hill <div>(relation: collaboration)</div></li></ul>"
            },
            "children": []
        }]
    }, {
        "id": "107877_3",
        "name": "Neil Young &amp; Pearl Jam",
        "data": {
            "relation": "<h4>Neil Young &amp; Pearl Jam</h4><b>Connections:</b><ul><li>Pearl Jam <div>(relation: collaboration)</div></li><li>Neil Young <div>(relation: collaboration)</div></li></ul>"
        },
        "children": [{
            "id": "964_4",
            "name": "Neil Young",
            "data": {
                "relation": "<h4>Neil Young</h4><b>Connections:</b><ul><li>Neil Young &amp; Pearl Jam <div>(relation: collaboration)</div></li></ul>"
            },
            "children": []
        }]
    }, {
        "id": "236797_5",
        "name": "Jeff Ament",
        "data": {
            "relation": "<h4>Jeff Ament</h4><b>Connections:</b><ul><li>Pearl Jam <div>(relation: member of band)</div></li><li>Temple of the Dog <div>(relation: member of band)</div></li><li>Mother Love Bone <div>(relation: member of band)</div></li><li>Green River <div>(relation: member of band)</div></li><li>M.A.C.C. <div>(relation: collaboration)</div></li><li>Three Fish <div>(relation: member of band)</div></li><li>Gossman Project <div>(relation: member of band)</div></li></ul>"
        },
        "children": [{
            "id": "1756_6",
            "name": "Temple of the Dog",
            "data": {
                "relation": "<h4>Temple of the Dog</h4><b>Connections:</b><ul><li>Jeff Ament <div>(relation: member of band)</div></li></ul>"
            },
            "children": []
        }, {
            "id": "14581_7",
            "name": "Mother Love Bone",
            "data": {
                "relation": "<h4>Mother Love Bone</h4><b>Connections:</b><ul><li>Jeff Ament <div>(relation: member of band)</div></li></ul>"
            },
            "children": []
        }, {
            "id": "50188_8",
            "name": "Green River",
            "data": {
                "relation": "<h4>Green River</h4><b>Connections:</b><ul><li>Jeff Ament <div>(relation: member of band)</div></li></ul>"
            },
            "children": []
        }, {
            "id": "65452_9",
            "name": "M.A.C.C.",
            "data": {
                "relation": "<h4>M.A.C.C.</h4><b>Connections:</b><ul><li>Jeff Ament <div>(relation: collaboration)</div></li></ul>"
            },
            "children": []
        }, {
            "id": "115632_10",
            "name": "Three Fish",
            "data": {
                "relation": "<h4>Three Fish</h4><b>Connections:</b><ul><li>Jeff Ament <div>(relation: member of band)</div></li></ul>"
            },
            "children": []
        }, {
            "id": "346850_11",
            "name": "Gossman Project",
            "data": {
                "relation": "<h4>Gossman Project</h4><b>Connections:</b><ul><li>Jeff Ament <div>(relation: member of band)</div></li></ul>"
            },
            "children": []
        }]
    }, {
        "id": "41529_12",
        "name": "Stone Gossard",
        "data": {
            "relation": "<h4>Stone Gossard</h4><b>Connections:</b><ul><li>Pearl Jam <div>(relation: member of band)</div></li><li>Temple of the Dog <div>(relation: member of band)</div></li><li>Mother Love Bone <div>(relation: member of band)</div></li><li>Brad <div>(relation: member of band)</div></li><li>Green River <div>(relation: member of band)</div></li><li>Gossman Project <div>(relation: member of band)</div></li></ul>"
        },
        "children": [{
            "id": "1756_13",
            "name": "Temple of the Dog",
            "data": {
                "relation": "<h4>Temple of the Dog</h4><b>Connections:</b><ul><li>Stone Gossard <div>(relation: member of band)</div></li></ul>"
            },
            "children": []
        }, {
            "id": "14581_14",
            "name": "Mother Love Bone",
            "data": {
                "relation": "<h4>Mother Love Bone</h4><b>Connections:</b><ul><li>Stone Gossard <div>(relation: member of band)</div></li></ul>"
            },
            "children": []
        }, {
            "id": "24119_15",
            "name": "Brad",
            "data": {
                "relation": "<h4>Brad</h4><b>Connections:</b><ul><li>Stone Gossard <div>(relation: member of band)</div></li></ul>"
            },
            "children": []
        }, {
            "id": "50188_16",
            "name": "Green River",
            "data": {
                "relation": "<h4>Green River</h4><b>Connections:</b><ul><li>Stone Gossard <div>(relation: member of band)</div></li></ul>"
            },
            "children": []
        }, {
            "id": "346850_17",
            "name": "Gossman Project",
            "data": {
                "relation": "<h4>Gossman Project</h4><b>Connections:</b><ul><li>Stone Gossard <div>(relation: member of band)</div></li></ul>"
            },
            "children": []
        }]
    }, {
        "id": "131161_18",
        "name": "Eddie Vedder",
        "data": {
            "relation": "<h4>Eddie Vedder</h4><b>Connections:</b><ul><li>Pearl Jam <div>(relation: member of band)</div></li><li>Temple of the Dog <div>(relation: member of band)</div></li><li>Eddie Vedder &amp; Zeke <div>(relation: collaboration)</div></li><li>Bad Radio <div>(relation: member of band)</div></li><li>Beck &amp; Eddie Vedder <div>(relation: collaboration)</div></li></ul>"
        },
        "children": [{
            "id": "1756_19",
            "name": "Temple of the Dog",
            "data": {
                "relation": "<h4>Temple of the Dog</h4><b>Connections:</b><ul><li>Eddie Vedder <div>(relation: member of band)</div></li></ul>"
            },
            "children": []
        }, {
            "id": "72007_20",
            "name": "Eddie Vedder &amp; Zeke",
            "data": {
                "relation": "<h4>Eddie Vedder &amp; Zeke</h4><b>Connections:</b><ul><li>Eddie Vedder <div>(relation: collaboration)</div></li></ul>"
            },
            "children": []
        }, {
            "id": "236657_21",
            "name": "Bad Radio",
            "data": {
                "relation": "<h4>Bad Radio</h4><b>Connections:</b><ul><li>Eddie Vedder <div>(relation: member of band)</div></li></ul>"
            },
            "children": []
        }, {
            "id": "432176_22",
            "name": "Beck &amp; Eddie Vedder",
            "data": {
                "relation": "<h4>Beck &amp; Eddie Vedder</h4><b>Connections:</b><ul><li>Eddie Vedder <div>(relation: collaboration)</div></li></ul>"
            },
            "children": []
        }]
    }, {
        "id": "236583_23",
        "name": "Mike McCready",
        "data": {
            "relation": "<h4>Mike McCready</h4><b>Connections:</b><ul><li>Pearl Jam <div>(relation: member of band)</div></li><li>Mad Season <div>(relation: member of band)</div></li><li>Temple of the Dog <div>(relation: member of band)</div></li><li>$10,000 Gold Chain <div>(relation: collaboration)</div></li><li>M.A.C.C. <div>(relation: collaboration)</div></li><li>The Rockfords <div>(relation: member of band)</div></li><li>Gossman Project <div>(relation: member of band)</div></li></ul>"
        },
        "children": [{
            "id": "1744_24",
            "name": "Mad Season",
            "data": {
                "relation": "<h4>Mad Season</h4><b>Connections:</b><ul><li>Mike McCready <div>(relation: member of band)</div></li></ul>"
            },
            "children": []
        }, {
            "id": "1756_25",
            "name": "Temple of the Dog",
            "data": {
                "relation": "<h4>Temple of the Dog</h4><b>Connections:</b><ul><li>Mike McCready <div>(relation: member of band)</div></li></ul>"
            },
            "children": []
        }, {
            "id": "43661_26",
            "name": "$10,000 Gold Chain",
            "data": {
                "relation": "<h4>$10,000 Gold Chain</h4><b>Connections:</b><ul><li>Mike McCready <div>(relation: collaboration)</div></li></ul>"
            },
            "children": []
        }, {
            "id": "65452_27",
            "name": "M.A.C.C.",
            "data": {
                "relation": "<h4>M.A.C.C.</h4><b>Connections:</b><ul><li>Mike McCready <div>(relation: collaboration)</div></li></ul>"
            },
            "children": []
        }, {
            "id": "153766_28",
            "name": "The Rockfords",
            "data": {
                "relation": "<h4>The Rockfords</h4><b>Connections:</b><ul><li>Mike McCready <div>(relation: member of band)</div></li></ul>"
            },
            "children": []
        }, {
            "id": "346850_29",
            "name": "Gossman Project",
            "data": {
                "relation": "<h4>Gossman Project</h4><b>Connections:</b><ul><li>Mike McCready <div>(relation: member of band)</div></li></ul>"
            },
            "children": []
        }]
    }, {
        "id": "236585_30",
        "name": "Matt Cameron",
        "data": {
            "relation": "<h4>Matt Cameron</h4><b>Connections:</b><ul><li>Pearl Jam <div>(relation: member of band)</div></li><li>Soundgarden <div>(relation: member of band)</div></li><li>Temple of the Dog <div>(relation: member of band)</div></li><li>Eleven <div>(relation: supporting musician)</div></li><li>Queens of the Stone Age <div>(relation: member of band)</div></li><li>Wellwater Conspiracy <div>(relation: member of band)</div></li><li>M.A.C.C. <div>(relation: collaboration)</div></li><li>Tone Dogs <div>(relation: member of band)</div></li></ul>"
        },
        "children": [{
            "id": "1111_31",
            "name": "Soundgarden",
            "data": {
                "relation": "<h4>Soundgarden</h4><b>Connections:</b><ul><li>Matt Cameron <div>(relation: member of band)</div></li></ul>"
            },
            "children": []
        }, {
            "id": "1756_32",
            "name": "Temple of the Dog",
            "data": {
                "relation": "<h4>Temple of the Dog</h4><b>Connections:</b><ul><li>Matt Cameron <div>(relation: member of band)</div></li></ul>"
            },
            "children": []
        }, {
            "id": "9570_33",
            "name": "Eleven",
            "data": {
                "relation": "<h4>Eleven</h4><b>Connections:</b><ul><li>Matt Cameron <div>(relation: supporting musician)</div></li></ul>"
            },
            "children": []
        }, {
            "id": "11783_34",
            "name": "Queens of the Stone Age",
            "data": {
                "relation": "<h4>Queens of the Stone Age</h4><b>Connections:</b><ul><li>Matt Cameron <div>(relation: member of band)</div></li></ul>"
            },
            "children": []
        }, {
            "id": "61972_35",
            "name": "Wellwater Conspiracy",
            "data": {
                "relation": "<h4>Wellwater Conspiracy</h4><b>Connections:</b><ul><li>Matt Cameron <div>(relation: member of band)</div></li></ul>"
            },
            "children": []
        }, {
            "id": "65452_36",
            "name": "M.A.C.C.",
            "data": {
                "relation": "<h4>M.A.C.C.</h4><b>Connections:</b><ul><li>Matt Cameron <div>(relation: collaboration)</div></li></ul>"
            },
            "children": []
        }, {
            "id": "353097_37",
            "name": "Tone Dogs",
            "data": {
                "relation": "<h4>Tone Dogs</h4><b>Connections:</b><ul><li>Matt Cameron <div>(relation: member of band)</div></li></ul>"
            },
            "children": []
        }]
    }, {
        "id": "236594_38",
        "name": "Dave Krusen",
        "data": {
            "relation": "<h4>Dave Krusen</h4><b>Connections:</b><ul><li>Pearl Jam <div>(relation: member of band)</div></li><li>Candlebox <div>(relation: member of band)</div></li></ul>"
        },
        "children": [{
            "id": "2092_39",
            "name": "Candlebox",
            "data": {
                "relation": "<h4>Candlebox</h4><b>Connections:</b><ul><li>Dave Krusen <div>(relation: member of band)</div></li></ul>"
            },
            "children": []
        }]
    }, {
        "id": "236022_40",
        "name": "Matt Chamberlain",
        "data": {
            "relation": "<h4>Matt Chamberlain</h4><b>Connections:</b><ul><li>Pearl Jam <div>(relation: member of band)</div></li><li>Critters Buggin <div>(relation: member of band)</div></li><li>Edie Brickell and New Bohemians <div>(relation: member of band)</div></li></ul>"
        },
        "children": [{
            "id": "54761_41",
            "name": "Critters Buggin",
            "data": {
                "relation": "<h4>Critters Buggin</h4><b>Connections:</b><ul><li>Matt Chamberlain <div>(relation: member of band)</div></li></ul>"
            },
            "children": []
        }, {
            "id": "92043_42",
            "name": "Edie Brickell and New Bohemians",
            "data": {
                "relation": "<h4>Edie Brickell and New Bohemians</h4><b>Connections:</b><ul><li>Matt Chamberlain <div>(relation: member of band)</div></li></ul>"
            },
            "children": []
        }]
    }, {
        "id": "236611_43",
        "name": "Dave Abbruzzese",
        "data": {
            "relation": "<h4>Dave Abbruzzese</h4><b>Connections:</b><ul><li>Pearl Jam <div>(relation: member of band)</div></li><li>Green Romance Orchestra <div>(relation: member of band)</div></li></ul>"
        },
        "children": [{
            "id": "276933_44",
            "name": "Green Romance Orchestra",
            "data": {
                "relation": "<h4>Green Romance Orchestra</h4><b>Connections:</b><ul><li>Dave Abbruzzese <div>(relation: member of band)</div></li></ul>"
            },
            "children": []
        }]
    }, {
        "id": "236612_45",
        "name": "Jack Irons",
        "data": {
            "relation": "<h4>Jack Irons</h4><b>Connections:</b><ul><li>Pearl Jam <div>(relation: member of band)</div></li><li>Redd Kross <div>(relation: member of band)</div></li><li>Eleven <div>(relation: member of band)</div></li><li>Red Hot Chili Peppers <div>(relation: member of band)</div></li><li>Anthym <div>(relation: member of band)</div></li><li>What Is This? <div>(relation: member of band)</div></li></ul>"
        },
        "children": [{
            "id": "4619_46",
            "name": "Redd Kross",
            "data": {
                "relation": "<h4>Redd Kross</h4><b>Connections:</b><ul><li>Jack Irons <div>(relation: member of band)</div></li></ul>"
            },
            "children": []
        }, {
            "id": "9570_47",
            "name": "Eleven",
            "data": {
                "relation": "<h4>Eleven</h4><b>Connections:</b><ul><li>Jack Irons <div>(relation: member of band)</div></li></ul>"
            },
            "children": []
        }, {
            "id": "12389_48",
            "name": "Red Hot Chili Peppers",
            "data": {
                "relation": "<h4>Red Hot Chili Peppers</h4><b>Connections:</b><ul><li>Jack Irons <div>(relation: member of band)</div></li></ul>"
            },
            "children": []
        }, {
            "id": "114288_49",
            "name": "Anthym",
            "data": {
                "relation": "<h4>Anthym</h4><b>Connections:</b><ul><li>Jack Irons <div>(relation: member of band)</div></li></ul>"
            },
            "children": []
        }, {
            "id": "240013_50",
            "name": "What Is This?",
            "data": {
                "relation": "<h4>What Is This?</h4><b>Connections:</b><ul><li>Jack Irons <div>(relation: member of band)</div></li></ul>"
            },
            "children": []
        }]
    }],
    "data": {
        "relation": "<h4>Pearl Jam</h4><b>Connections:</b><ul><li>Pearl Jam &amp; Cypress Hill <div>(relation: collaboration)</div></li><li>Neil Young &amp; Pearl Jam <div>(relation: collaboration)</div></li><li>Jeff Ament <div>(relation: member of band)</div></li><li>Stone Gossard <div>(relation: member of band)</div></li><li>Eddie Vedder <div>(relation: member of band)</div></li><li>Mike McCready <div>(relation: member of band)</div></li><li>Matt Cameron <div>(relation: member of band)</div></li><li>Dave Krusen <div>(relation: member of band)</div></li><li>Matt Chamberlain <div>(relation: member of band)</div></li><li>Dave Abbruzzese <div>(relation: member of band)</div></li><li>Jack Irons <div>(relation: member of band)</div></li></ul>"
    }
}
SunburstJSONSampleData = {
 "children": [
     {
       "children": [
         {
           "children": [],
           "data": {
             "description": "",
             "$angularWidth": 7490,
             "days": 111,
             "$color": "#FCD9A1",
             "size": 7490
           },
           "id": "Source/Coordinates/Complex.js",
           "name": "Complex.js"
         },
         {
           "children": [],
           "data": {
             "description": "Fixed polar interpolation problem when theta = pi",
             "$angularWidth": 6390,
             "days": 2,
             "$color": "#B0AAF6",
             "size": 6390
           },
           "id": "Source/Coordinates/Polar.js",
           "name": "Polar.js"
         }
       ],
       "data": {
         "description": "Fixed polar interpolation problem when theta = pi",
         "$color": "#B0AAF6",
         "days": 2,
         "$angularWidth": 1000,
         "size": 13880
       },
       "id": "Source/Coordinates",
       "name": "Coordinates"
     },
     {
       "children": [
         {
           "children": [],
           "data": {
             "description": "Scaling done right :)",
             "$angularWidth": 14952,
             "days": 3,
             "$color": "#B2ABF4",
             "size": 14952
           },
           "id": "Source/Core/Canvas.js",
           "name": "Canvas.js"
         },
         {
           "children": [],
           "data": {
             "description": "Animated TreeMaps",
             "$angularWidth": 14759,
             "days": 3,
             "$color": "#B2ABF4",
             "size": 14759
           },
           "id": "Source/Core/Core.js",
           "name": "Core.js"
         },
         {
           "children": [],
           "data": {
             "description": "",
             "$angularWidth": 5838,
             "days": 111,
             "$color": "#FCD9A1",
             "size": 5838
           },
           "id": "Source/Core/Fx.js",
           "name": "Fx.js"
         }
       ],
       "data": {
         "description": "Animated TreeMaps",
         "$color": "#B2ABF4",
         "days": 3,
         "$angularWidth": 1000,
         "size": 35549
       },
       "id": "Source/Core",
       "name": "Core"
     },
     {
       "children": [
         {
           "children": [],
           "data": {
             "description": "Merge remote branch 'woot/bugfixes_docnet' into sunburst_fixes",
             "$angularWidth": 18672,
             "days": 1,
             "$color": "#AEA9F8",
             "size": 18672
           },
           "id": "Source/Extras/Extras.js",
           "name": "Extras.js"
         }
       ],
       "data": {
         "description": "Merge remote branch 'woot/bugfixes_docnet' into sunburst_fixes",
         "$color": "#AEA9F8",
         "days": 1,
         "$angularWidth": 1000,
         "size": 18672
       },
       "id": "Source/Extras",
       "name": "Extras"
     },
     {
       "children": [
         {
           "children": [],
           "data": {
             "description": "Animated TreeMaps",
             "$angularWidth": 1652,
             "days": 3,
             "$color": "#B2ABF4",
             "size": 1652
           },
           "id": "Source/Graph/Graph.Geom.js",
           "name": "Graph.Geom.js"
         },
         {
           "children": [],
           "data": {
             "description": "Animated TreeMaps",
             "$angularWidth": 27921,
             "days": 3,
             "$color": "#B2ABF4",
             "size": 27921
           },
           "id": "Source/Graph/Graph.js",
           "name": "Graph.js"
         },
         {
           "children": [],
           "data": {
             "description": "Added new Canvas class with zoom/pan options",
             "$angularWidth": 9512,
             "days": 5,
             "$color": "#B6AEEF",
             "size": 9512
           },
           "id": "Source/Graph/Graph.Label.js",
           "name": "Graph.Label.js"
         },
         {
           "children": [],
           "data": {
             "description": "Change the way edges where stored and used in Graph.js. This is how Graph.js internally handles nodes. The user API should remain the same.",
             "$angularWidth": 22838,
             "days": 26,
             "$color": "#E0C7C0",
             "size": 22838
           },
           "id": "Source/Graph/Graph.Op.js",
           "name": "Graph.Op.js"
         },
         {
           "children": [],
           "data": {
             "description": "Bug Fix Extras + Tweaking examples",
             "$angularWidth": 18950,
             "days": 19,
             "$color": "#D2BFD0",
             "size": 18950
           },
           "id": "Source/Graph/Graph.Plot.js",
           "name": "Graph.Plot.js"
         },
         {
           "children": [],
           "data": {
             "description": "(Re)-Implemented nodeTypes",
             "$angularWidth": 6947,
             "days": 32,
             "$color": "#ECCFB3",
             "size": 6947
           },
           "id": "Source/Graph/Helpers.js",
           "name": "Helpers.js"
         }
       ],
       "data": {
         "description": "Animated TreeMaps",
         "$color": "#B2ABF4",
         "days": 3,
         "$angularWidth": 1000,
         "size": 87820
       },
       "id": "Source/Graph",
       "name": "Graph"
     },
     {
       "children": [
         {
           "children": [],
           "data": {
             "description": "$jit namespace",
             "$angularWidth": 4064,
             "days": 111,
             "$color": "#FCD9A1",
             "size": 4064
           },
           "id": "Source/Layouts/Layouts.ForceDirected.js",
           "name": "Layouts.ForceDirected.js"
         },
         {
           "children": [],
           "data": {
             "description": "Animated TreeMaps",
             "$angularWidth": 2198,
             "days": 3,
             "$color": "#B2ABF4",
             "size": 2198
           },
           "id": "Source/Layouts/Layouts.js",
           "name": "Layouts.js"
         },
         {
           "children": [],
           "data": {
             "description": "$jit namespace",
             "$angularWidth": 4372,
             "days": 111,
             "$color": "#FCD9A1",
             "size": 4372
           },
           "id": "Source/Layouts/Layouts.Radial.js",
           "name": "Layouts.Radial.js"
         },
         {
           "children": [],
           "data": {
             "description": "Animated TreeMaps",
             "$angularWidth": 15570,
             "days": 3,
             "$color": "#B2ABF4",
             "size": 15570
           },
           "id": "Source/Layouts/Layouts.TM.js",
           "name": "Layouts.TM.js"
         },
         {
           "children": [],
           "data": {
             "description": "$jit namespace",
             "$angularWidth": 6696,
             "days": 111,
             "$color": "#FCD9A1",
             "size": 6696
           },
           "id": "Source/Layouts/Layouts.Tree.js",
           "name": "Layouts.Tree.js"
         }
       ],
       "data": {
         "description": "Animated TreeMaps",
         "$color": "#B2ABF4",
         "days": 3,
         "$angularWidth": 1000,
         "size": 32900
       },
       "id": "Source/Layouts",
       "name": "Layouts"
     },
     {
       "children": [
         {
           "children": [],
           "data": {
             "description": "Fixed passing of general Label object",
             "$angularWidth": 8079,
             "days": 26,
             "$color": "#E0C7C0",
             "size": 8079
           },
           "id": "Source/Loader/Loader.js",
           "name": "Loader.js"
         }
       ],
       "data": {
         "description": "Fixed passing of general Label object",
         "$color": "#E0C7C0",
         "days": 26,
         "$angularWidth": 1000,
         "size": 8079
       },
       "id": "Source/Loader",
       "name": "Loader"
     },
     {
       "children": [
         {
           "children": [],
           "data": {
             "description": "Small tweaks on Tips and Selected nodes in Charts",
             "$angularWidth": 348,
             "days": 33,
             "$color": "#EED0B0",
             "size": 348
           },
           "id": "Source/Options/Options.AreaChart.js",
           "name": "Options.AreaChart.js"
         },
         {
           "children": [],
           "data": {
             "description": "Added gradients to AreaChart",
             "$angularWidth": 386,
             "days": 37,
             "$color": "#F6D5A7",
             "size": 386
           },
           "id": "Source/Options/Options.BarChart.js",
           "name": "Options.BarChart.js"
         },
         {
           "children": [],
           "data": {
             "description": "Add label types",
             "$angularWidth": 392,
             "days": 26,
             "$color": "#E0C7C0",
             "size": 392
           },
           "id": "Source/Options/Options.Canvas.js",
           "name": "Options.Canvas.js"
         },
         {
           "children": [],
           "data": {
             "description": "Organizing sources and build",
             "$angularWidth": 3856,
             "days": 112,
             "$color": "#FCD9A1",
             "size": 3856
           },
           "id": "Source/Options/Options.Controller.js",
           "name": "Options.Controller.js"
         },
         {
           "children": [],
           "data": {
             "description": "Added raw Canvas options ",
             "$angularWidth": 1475,
             "days": 31,
             "$color": "#EACDB5",
             "size": 1475
           },
           "id": "Source/Options/Options.Edge.js",
           "name": "Options.Edge.js"
         },
         {
           "children": [],
           "data": {
             "description": "Extras.Events bug fixes",
             "$angularWidth": 312,
             "days": 20,
             "$color": "#D4C0CE",
             "size": 312
           },
           "id": "Source/Options/Options.Events.js",
           "name": "Options.Events.js"
         },
         {
           "children": [],
           "data": {
             "description": "$jit namespace",
             "$angularWidth": 749,
             "days": 111,
             "$color": "#FCD9A1",
             "size": 749
           },
           "id": "Source/Options/Options.Fx.js",
           "name": "Options.Fx.js"
         },
         {
           "children": [],
           "data": {
             "description": "Revisiting Extras.js",
             "$angularWidth": 530,
             "days": 25,
             "$color": "#DEC6C2",
             "size": 530
           },
           "id": "Source/Options/Options.js",
           "name": "Options.js"
         },
         {
           "children": [],
           "data": {
             "description": "Add label types",
             "$angularWidth": 203,
             "days": 26,
             "$color": "#E0C7C0",
             "size": 203
           },
           "id": "Source/Options/Options.Label.js",
           "name": "Options.Label.js"
         },
         {
           "children": [],
           "data": {
             "description": "* Ignore panning",
             "$angularWidth": 137,
             "days": 1,
             "$color": "#AEA9F8",
             "size": 137
           },
           "id": "Source/Options/Options.Navigation.js",
           "name": "Options.Navigation.js"
         },
         {
           "children": [],
           "data": {
             "description": "Added raw Canvas options",
             "$angularWidth": 2083,
             "days": 31,
             "$color": "#EACDB5",
             "size": 2083
           },
           "id": "Source/Options/Options.Node.js",
           "name": "Options.Node.js"
         },
         {
           "children": [],
           "data": {
             "description": "Bug Fix Extras + Tweaking examples",
             "$angularWidth": 583,
             "days": 19,
             "$color": "#D2BFD0",
             "size": 583
           },
           "id": "Source/Options/Options.NodeStyles.js",
           "name": "Options.NodeStyles.js"
         },
         {
           "children": [],
           "data": {
             "description": "Add an option to resize labels according to its pie slice",
             "$angularWidth": 380,
             "days": 1,
             "$color": "#AEA9F8",
             "size": 380
           },
           "id": "Source/Options/Options.PieChart.js",
           "name": "Options.PieChart.js"
         },
         {
           "children": [],
           "data": {
             "description": "Revisiting Extras.js RedesigningMouseEventManager",
             "$angularWidth": 1120,
             "days": 25,
             "$color": "#DEC6C2",
             "size": 1120
           },
           "id": "Source/Options/Options.Tips.js",
           "name": "Options.Tips.js"
         },
         {
           "children": [],
           "data": {
             "description": "Organizing sources and build",
             "$angularWidth": 1021,
             "days": 112,
             "$color": "#FCD9A1",
             "size": 1021
           },
           "id": "Source/Options/Options.Tree.js",
           "name": "Options.Tree.js"
         }
       ],
       "data": {
         "description": "Add an option to resize labels according to its pie slice",
         "$color": "#AEA9F8",
         "days": 1,
         "$angularWidth": 1000,
         "size": 13575
       },
       "id": "Source/Options",
       "name": "Options"
     },
     {
       "children": [
         {
           "children": [],
           "data": {
             "description": "Fixing AreaCharts for IE",
             "$angularWidth": 13636,
             "days": 19,
             "$color": "#D2BFD0",
             "size": 13636
           },
           "id": "Source/Visualizations/AreaChart.js",
           "name": "AreaChart.js"
         },
         {
           "children": [],
           "data": {
             "description": "Append utils, id and Class objects to $jit. Add legends to Bar/Pie/AreaChart examples.",
             "$angularWidth": 12608,
             "days": 15,
             "$color": "#CABAD9",
             "size": 12608
           },
           "id": "Source/Visualizations/BarChart.js",
           "name": "BarChart.js"
         },
         {
           "children": [],
           "data": {
             "description": "Added new Canvas class with zoom/pan options",
             "$angularWidth": 16954,
             "days": 5,
             "$color": "#B6AEEF",
             "size": 16954
           },
           "id": "Source/Visualizations/ForceDirected.js",
           "name": "ForceDirected.js"
         },
         {
           "children": [],
           "data": {
             "description": "Added new Canvas class with zoom/pan options",
             "$angularWidth": 23448,
             "days": 5,
             "$color": "#B6AEEF",
             "size": 23448
           },
           "id": "Source/Visualizations/Hypertree.js",
           "name": "Hypertree.js"
         },
         {
           "children": [],
           "data": {
             "description": "Adding $jit as Namespace + Build Refactor + Config (part I)",
             "$angularWidth": 0,
             "days": 112,
             "$color": "#FCD9A1",
             "size": 0
           },
           "id": "Source/Visualizations/Icicle.js",
           "name": "Icicle.js"
         },
         {
           "children": [],
           "data": {
             "description": "Add an option to resize labels according to its pie slice",
             "$angularWidth": 10762,
             "days": 1,
             "$color": "#AEA9F8",
             "size": 10762
           },
           "id": "Source/Visualizations/PieChart.js",
           "name": "PieChart.js"
         },
         {
           "children": [],
           "data": {
             "description": "Added new Canvas class with zoom/pan options",
             "$angularWidth": 18010,
             "days": 5,
             "$color": "#B6AEEF",
             "size": 18010
           },
           "id": "Source/Visualizations/RGraph.js",
           "name": "RGraph.js"
         },
         {
           "children": [],
           "data": {
             "description": "Animated TreeMaps",
             "$angularWidth": 52895,
             "days": 3,
             "$color": "#B2ABF4",
             "size": 52895
           },
           "id": "Source/Visualizations/Spacetree.js",
           "name": "Spacetree.js"
         },
         {
           "children": [],
           "data": {
             "description": "Adding new JSON data to the Sunburst and already finding some bugs :S",
             "$angularWidth": 21436,
             "days": 2,
             "$color": "#B0AAF6",
             "size": 21436
           },
           "id": "Source/Visualizations/Sunburst.js",
           "name": "Sunburst.js"
         },
         {
           "children": [],
           "data": {
             "description": "Animated TreeMaps",
             "$angularWidth": 16472,
             "days": 3,
             "$color": "#B2ABF4",
             "size": 16472
           },
           "id": "Source/Visualizations/Treemap.js",
           "name": "Treemap.js"
         }
       ],
       "data": {
         "description": "Merge remote branch 'woot/bugfixes_docnet' into sunburst_fixes",
         "$color": "#AEA9F8",
         "days": 1,
         "$angularWidth": 1000,
         "size": 186221
       },
       "id": "Source/Visualizations",
       "name": "Visualizations"
     }
   ],
   "data": {
     "$type": "none"
   },
   "id": "Source",
   "name": "Source"
}
HyperTreeJSONSampleData = {
        "id": "347_0",
        "name": "Nine Inch Nails",
        "children": [{
            "id": "126510_1",
            "name": "Jerome Dillon",
            "data": {
                "band": "Nine Inch Nails",
                "relation": "member of band"
            },
            "children": [{
                "id": "52163_2",
                "name": "Howlin' Maggie",
                "data": {
                    "band": "Jerome Dillon",
                    "relation": "member of band"
                },
                "children": []
            }, {
                "id": "324134_3",
                "name": "nearLY",
                "data": {
                    "band": "Jerome Dillon",
                    "relation": "member of band"
                },
                "children": []
            }]
        }, {
            "id": "173871_4",
            "name": "Charlie Clouser",
            "data": {
                "band": "Nine Inch Nails",
                "relation": "member of band"
            },
            "children": []
        }, {
            "id": "235952_5",
            "name": "James Woolley",
            "data": {
                "band": "Nine Inch Nails",
                "relation": "member of band"
            },
            "children": []
        }, {
            "id": "235951_6",
            "name": "Jeff Ward",
            "data": {
                "band": "Nine Inch Nails",
                "relation": "member of band"
            },
            "children": [{
                "id": "2382_7",
                "name": "Ministry",
                "data": {
                    "band": "Jeff Ward",
                    "relation": "member of band"
                },
                "children": []
            }, {
                "id": "2415_8",
                "name": "Revolting Cocks",
                "data": {
                    "band": "Jeff Ward",
                    "relation": "member of band"
                },
                "children": []
            }, {
                "id": "3963_9",
                "name": "Pigface",
                "children": []
            }, {
                "id": "7848_10",
                "name": "Lard",
                "data": {
                    "band": "Jeff Ward",
                    "relation": "member of band"
                },
                "children": []
            }]
        }, {
            "id": "235950_11",
            "name": "Richard Patrick",
            "data": {
                "band": "Nine Inch Nails",
                "relation": "member of band"
            },
            "children": [{
                "id": "1007_12",
                "name": "Filter",
                "data": {
                    "band": "Richard Patrick",
                    "relation": "member of band"
                },
                "children": []
            }, {
                "id": "327924_13",
                "name": "Army of Anyone",
                "data": {
                    "band": "Richard Patrick",
                    "relation": "member of band"
                },
                "children": []
            }]
        }, {
            "id": "2396_14",
            "name": "Trent Reznor",
            "data": {
                "band": "Nine Inch Nails",
                "relation": "member of band"
            },
            "children": [{
                "id": "3963_15",
                "name": "Pigface",
                "data": {
                    "band": "Trent Reznor",
                    "relation": "member of band"
                },
                "children": []
            }, {
                "id": "32247_16",
                "name": "1000 Homo DJs",
                "data": {
                    "band": "Trent Reznor",
                    "relation": "member of band"
                },
                "children": []
            }, {
                "id": "83761_17",
                "name": "Option 30",
                "data": {
                    "band": "Trent Reznor",
                    "relation": "member of band"
                },
                "children": []
            }, {
                "id": "133257_18",
                "name": "Exotic Birds",
                "data": {
                    "band": "Trent Reznor",
                    "relation": "member of band"
                },
                "children": []
            }]
        }, {
            "id": "36352_19",
            "name": "Chris Vrenna",
            "data": {
                "band": "Nine Inch Nails",
                "relation": "member of band"
            },
            "children": [{
                "id": "1013_20",
                "name": "Stabbing Westward",
                "data": {
                    "band": "Chris Vrenna",
                    "relation": "member of band"
                },
                "children": []
            }, {
                "id": "3963_21",
                "name": "Pigface",
                "data": {
                    "band": "Chris Vrenna",
                    "relation": "member of band"
                },
                "children": []
            }, {
                "id": "5752_22",
                "name": "Jack Off Jill",
                "data": {
                    "band": "Chris Vrenna",
                    "relation": "member of band"
                },
                "children": []
            }, {
                "id": "33602_23",
                "name": "Die Warzau",
                "data": {
                    "band": "Chris Vrenna",
                    "relation": "member of band"
                },
                "children": []
            }, {
                "id": "40485_24",
                "name": "tweaker",
                "data": {
                    "band": "Chris Vrenna",
                    "relation": "is person"
                },
                "children": []
            }, {
                "id": "133257_25",
                "name": "Exotic Birds",
                "data": {
                    "band": "Chris Vrenna",
                    "relation": "member of band"
                },
                "children": []
            }]
        }, {
            "id": "236021_26",
            "name": "Aaron North",
            "data": {
                "band": "Nine Inch Nails",
                "relation": "member of band"
            },
            "children": []
        }, {
            "id": "236024_27",
            "name": "Jeordie White",
            "data": {
                "band": "Nine Inch Nails",
                "relation": "member of band"
            },
            "children": [{
                "id": "909_28",
                "name": "A Perfect Circle",
                "data": {
                    "band": "Jeordie White",
                    "relation": "member of band"
                },
                "children": []
            }, {
                "id": "237377_29",
                "name": "Twiggy Ramirez",
                "data": {
                    "band": "Jeordie White",
                    "relation": "is person"
                },
                "children": []
            }]
        }, {
            "id": "235953_30",
            "name": "Robin Finck",
            "data": {
                "band": "Nine Inch Nails",
                "relation": "member of band"
            },
            "children": [{
                "id": "1440_31",
                "name": "Guns N' Roses",
                "data": {
                    "band": "Robin Finck",
                    "relation": "member of band"
                },
                "children": []
            }]
        }, {
            "id": "235955_32",
            "name": "Danny Lohner",
            "data": {
                "band": "Nine Inch Nails",
                "relation": "member of band"
            },
            "children": [{
                "id": "909_33",
                "name": "A Perfect Circle",
                "data": {
                    "band": "Danny Lohner",
                    "relation": "member of band"
                },
                "children": []
            }, {
                "id": "1695_34",
                "name": "Killing Joke",
                "data": {
                    "band": "Danny Lohner",
                    "relation": "member of band"
                },
                "children": []
            }, {
                "id": "1938_35",
                "name": "Methods of Mayhem",
                "data": {
                    "band": "Danny Lohner",
                    "relation": "member of band"
                },
                "children": []
            }, {
                "id": "5138_36",
                "name": "Skrew",
                "data": {
                    "band": "Danny Lohner",
                    "relation": "member of band"
                },
                "children": []
            }, {
                "id": "53549_37",
                "name": "Angkor Wat",
                "data": {
                    "band": "Danny Lohner",
                    "relation": "member of band"
                },
                "children": []
            }, {
                "id": "113510_38",
                "name": "Puscifer",
                "data": {
                    "band": "Danny Lohner",
                    "relation": "member of band"
                },
                "children": []
            }, {
                "id": "113512_39",
                "name": "Renhold\u00ebr",
                "data": {
                    "band": "Danny Lohner",
                    "relation": "is person"
                },
                "children": []
            }]
        }],
        "data": []
    }



