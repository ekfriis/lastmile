from ants.graph.destination import Destination
from ants.metric import metric

if __name__ == "__main__":
    metric.loud()

metric.load()

destinations = [Destination(address) for address in 
      ['1400 WASHINGTON ST #1, SAN FRANCISCO, CA',
       '1824 JACKSON   STREET B, SAN FRANCISCO, CA',
       '1740 BROADWAY APT. 204, SAN FRANCISCO, CA',
       '1690 BROADWAY STREET APT. 710, SAN FRANCISCO, CA',
       '1901 PACIFIC #8, SAN FRANCISCO, CA',
       '1700 CALIFORNIA STREET APT 708, SAN FRANCISCO, CA',
       '1505 GOUGH ST. #17, SAN FRANCISCO, CA',
       '880 BUSH APT 415, SAN FRANCISCO, CA',
       '1428 WASHINGTON ST., SAN FRANCISCO, CA',
       '900 BUSH STREET APARTMENT 718, SAN FRANCISCO, CA',
       '1248 UNION STREET, SAN FRANCISCO, CA',
       '910 BAY STREET APT # 5, SAN FRANCISCO, CA',
       '1075 LOMBARD STREET, SAN FRANCISCO, CA',
       '1001 PINE STREET #605, SAN FRANCISCO, CA',
       '1701 JACKSON   STREET #609, SAN FRANCISCO, CA' ]]

metric.save()
