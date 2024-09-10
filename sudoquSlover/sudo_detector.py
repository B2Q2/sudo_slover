#/sudo_decoder

from sudo_structure import *
from sudo_display import *
from typing import List, Set

class Detector:

    def __init__(self, sudo_board:Board) -> None:
        self.sudo_board:Board = sudo_board
        self.block_region: List[Region] = []
        self.operation_region: List[Region] = sudo_board.MAP_OF_REGION
        self.scan()

    def scan(self):
        cycle_work = True
        while cycle_work:
            # if clear value was detected, cycle will be restet
            cycle_work = False

            # move for all region
            for region in self.operation_region:
                if region.value != 0 and not(region in self.block_region):
                    #new operation cycle
                    cycle_work = True

                    # remove region with set value, less operation
                    self.block_region.append( region )

                    # # cheange possibilites in structure
                    for sector_region in region.sector.REGION_IN_SECTOR:
                        if sector_region in self.operation_region:
                            sector_region.remove_possibilites( region.value )
                    
                    for line_region in region.line_horizontal.REGION_IN_LINE:
                        if sector_region in self.operation_region:
                            line_region.remove_possibilites( region.value )
                    
                    for line_region in region.line_vertical.REGION_IN_LINE:
                        if sector_region in self.operation_region:
                            line_region.remove_possibilites( region.value )
            else:
                pass
    
    def lineholider(self) -> None:

        all_lines = self.sudo_board.MAP_OF_HORIZONTAL_LINE + self.sudo_board.MAP_OF_VERTICAL_LINE
        for line in all_lines:
            
            operatin_region: Set[Region] = set()
            accounting: List[ Tuple[int, Sector] ] = []

            # load form line (value, sector, region)
            for region in line.REGION_IN_LINE:
                if not( region in self.block_region ):
                    operatin_region.add( region )

                    acc = [ (possib, region.sector) for possib in region.possibilites ]
                    accounting.extend(acc)
            else:
                # slove! problem with full line
                if accounting.__len__() == 0:
                    continue

            # eliminate duplicates
            accounting = list( set(accounting) )

            # find unic values in line
            values, _ = zip(*accounting)

            for value, sector in accounting:
                # if selected value is unice in line send to all psibilities in his sector to remove it
                if values.count( value ) == 1:
                    for region in sector.REGION_IN_SECTOR:
                        if not (region in operatin_region) and not(region in self.block_region):
                            region.remove_possibilites( value )

            del values, accounting, operatin_region
        
    def ultimateone(self) -> None:
        for sector in self.sudo_board.MAP_OF_SECTOR:

            accounting: List[ Tuple[int, Region] ] = []   

            for region in sector.REGION_IN_SECTOR:
                if not( region in self.block_region ):
                    acc = [ (possib, region) for possib in region.possibilites ]
                    accounting.extend(acc)
            else:
                # slove! problem with full line
                if accounting.__len__() == 0:
                    continue

            # find unic values
            values, _ = zip(*accounting)
            for acc in accounting:
                value = acc[0]
                region = acc[1]
                if values.count( value ) == 1:
                    region.set_value( value )

            del accounting
        
    def pairinline(self) -> None:
        all_lines = self.sudo_board.MAP_OF_HORIZONTAL_LINE + self.sudo_board.MAP_OF_VERTICAL_LINE
        for line in all_lines:
            
            operatin_region: Set[Region] = set()
            grupe_by_regions: Dict[ Region, List] = dict()

            # load form line (value, sector, region)
            for region in line.REGION_IN_LINE:
                if not( region in self.block_region ):
                    operatin_region.add( region )

                    grupe_by_regions[region] = region.possibilites
            else:
                if grupe_by_regions.__len__() == 0:
                    continue

            # search grupe_by_values to find identical pair (n, m)
            ''' special condition:
            
            if line have to Region with only 2 decision and have uncertain Regions 
            thats Regions Shuld have eliminate from this Regions taht 2 posibilites
            
            ''' 
            duble_value: List[int, int] = None
            work_region: Set = set()

            # print(line)
            # for key in grupe_by_regions:
            #     print( f"{key}: {grupe_by_regions[key]}")

            for region_in_grupe, value_pair in grupe_by_regions.items():
                
                if value_pair.__len__() == 2:
                    # pair was found
                    if isinstance(duble_value, list):
                        # if the same pair
                        if value_pair == duble_value:
                            work_region.add( region_in_grupe )

                            for region in line.REGION_IN_LINE:
                                if (not(region in work_region)) and (region in operatin_region):
                                    region.remove_possibilites( duble_value[0] )
                                    region.remove_possibilites( duble_value[1] )
                            break

                    # to pair exist  
                    if list( grupe_by_regions.values() ).count( value_pair ) == 2:
                        duble_value = value_pair
                        work_region.add( region_in_grupe )

            del duble_value, work_region, operatin_region    
        pass


    def sudo_slove(self) -> bool:
        if self.block_region.__len__() == 81:
            return True
        else:
            return False