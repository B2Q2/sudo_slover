#/size

class Size():
    def __init__(self, width:int, hight:int) -> None:
        assert Size.Check_is_natural_number(width), "Err.. Size can not be unnatural number!"
        assert Size.Check_is_natural_number(hight), "Err.. Size can not be unnatural number!"
        self.width: int = width
        self.hight: int = hight

    def scale(self, scale:int|float ) -> None:
        assert Size.Check_is_scale(scale), "Err.. Scale must be positive value!"
        self.width:int = int(self.width * scale)
        self.hight: int = int(self.hight * scale)
    
    def resize(self, scale_width:int, scale_hight:int) -> None:
        assert Size.Check_is_scale(scale_width), "Err.. Scale must be positive value!"
        assert Size.Check_is_scale(scale_hight), "Err.. Scale must be positive value!"
        self.width:int = int(self.width * scale_width)
        self.hight: int = int(self.hight * scale_hight)

    def new(self, new_width:int, new_hight:int) -> None:
        self.__init__(new_width, new_hight)

    def data_storage(self) -> int:
        return self.width * self.hight

    def __str__(self) -> str:
        return "({0}, {1})".format(self.width, self.hight)

    @staticmethod
    def Check_is_natural_number(value:int) -> bool:
        return  isinstance(value, int) and (value > 0)
    
    @staticmethod
    def Check_is_scale(value:int|float) -> bool:
        return (isinstance(value, int) or isinstance(value, float)) and (value > 0)
    

if __name__ == "__main__":
    foo = Size(1,2)
    print(foo)
    foo.resize(4,5)
    print(foo)
    foo.scale(3)
    print(foo)
    foo.new(9,12)
    print(foo)
    foo.scale(1/3)
    print(foo)