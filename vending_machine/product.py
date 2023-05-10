from .vendingmachine import *
from .textformatter import TextFormatter

__all__ = ['Product']

class Product():
    def __init__(self, ID: int, name: str, price: int, count: int = 0, product_type: str = None) -> None:
        """
        상품 객체를 초기화하는 메서드입니다.

        Args:
            ID (int): 상품 ID
            name (str): 상품 이름    
            price (int): 상품 가격
            count (int, optional): 상품 수량. 기본값은 0.
            product_type (str, optional): 상품 종류. 기본값은 None.
        """
        self.id: int = ID
        self.name: str = name
        self.price: int = price
        self.count: int = count
        self.product_type: str = product_type

    
    def __int__(self) -> int:
        return self.id

    def __str__(self) -> str:
        return self.name

    @property
    def is_empty(self) -> bool:
        """
        상품의 수량이 0인지 확인하는 프로퍼티
        """
        return self.count < 1
    
    @property
    def to_dict(self):
        """
        상품 객체를 딕셔너리로 반환하는 프로퍼티
        """
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'count': self.count,
        }
    
    def product_info(self, VM : 'VendingMachine' = None, check_money: bool = True, manage_mod: bool = False) -> str:
        """
        상품의 정보를 문자열로 반환하는 메서드입니다.
        
        args:
            VM (VendingMachine): 자판기 객체
            check_money (bool): 잔돈 부족 여부를 확인할지 여부
            manage_mod (bool): 관리자 모드인지 여부
        
        returns:
            str: 상품의 정보
        """
        prod_name = TextFormatter.fill_str_with_space(self.name)
        if manage_mod: # 관리자 모드인 경우
            return f'{self.id:>2d}. {prod_name} : {self.price:>5}원, {self.count:>3d}개'
        elif self.is_empty: # 상품이 품절된 경우
            return TextFormatter.textColor(f'{self.id:>2d}. {prod_name} : {"품절":>5}', 'red') # 품절 표시를 빨간색으로 표시
        elif not VM.is_sellable(self) and check_money: # 잔돈 부족인 경우
            return TextFormatter.textColor(f'{self.id:>2d}. {prod_name} : {"잔돈 부족":>5}', 'red') # 잔돈 부족 표시를 빨간색으로 표시
        return f'{self.id:>2d}. {prod_name} : {self.price:>5}원' 
