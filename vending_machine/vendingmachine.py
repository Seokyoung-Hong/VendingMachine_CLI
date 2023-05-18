from .product import Product
import datetime

__all__ = ['VendingMachine', 'VendingMachineUser']



class VendingMachineUser(): 
    def __init__(self) -> None:
        """
        VendingMachine 사용자 클래스입니다.

        Attributes:
            money_box (dict): 사용자가 보유한 돈의 갯수를 나타내는 딕셔너리. 돈의 종류를 key로, 갯수를 value로 가집니다.
            credit_money (int): 사용자의 신용 금액을 나타내는 변수. 기본값은 10000입니다.
            selected_product (Product): 사용자가 선택한 상품을 나타내는 변수. 기본값은 None입니다.
            is_credit (bool): 신용 결제 모드 여부를 나타내는 변수. 기본값은 False입니다.
        """
        self.money_box: dict[int:int] = {100: 4, 500: 2, 1000: 4}
        self.credit_money: int = 10000
        self.is_credit: bool = False

    def reset(self) -> None:
        """
        사용자의 돈 보유 상태와 선택한 구매방법을 초기화하는 메서드입니다.
        """
        self.money_box: dict[int:int] = {100: 4, 500: 2, 1000: 4}
        self.credit_money: int = 10000
        self.is_credit: bool = False

        return None

    
    @property
    def total_money(self) -> int:
        """
        사용자의 총 보유 금액을 계산하여 반환하는 프로퍼티입니다.
        
        Returns:
            int: 사용자의 총 보유 금액
        """
        if self.is_credit:
            return self.credit_money
        return sum((k*v for k,v in self.money_box.items())) # 딕셔너리의 key와 value를 각각 곱한 후 모두 더함

    @property
    def status(self) -> str:
        """
        현재 사용자의 잔돈 정보를 문자열로 반환하는 메서드입니다.
        
        Returns:
            str: 현재 사용자의 잔돈 정보를 나타내는 문자열
        """
        if self.is_credit:
            return f'잔액 : {self.credit_money}'
        return f'1000원 : {self.money_box[1000]}개   500원 : {self.money_box[500]}개   100원 : {self.money_box[100]}개'






class VendingMachine(BaseException):
    def __init__(self, file: str) -> None:
        """
        자판기 클래스의 생성자

        Args:
            file (str, optional): JSON 파일명. Defaults to None.
        """
        self.products: list[Product] = []               # 자판기에 등록된 상품들을 담을 리스트
        self.change_box: dict[int:int] = {100 : 10, 500 : 10, 1000 : 0}   # 거스름돈 보관함
        self.inserted_money: int = 0          # 사용자가 투입한 금액
        self.user: VendingMachineUser = VendingMachineUser()   # 자판기 사용자
        self.report_file: str = 'report.txt'   # 자판기 리포트 파일명
        self.products_file = file
        self.products_by_json()   # JSON 파일을 통해 상품들을 등록하는 메소드 호출
    
    @property
    def change_box_info(self):
        return f'100원 : {self.change_box[100]}개   500원 : {self.change_box[500]}개   1000원 : {self.change_box[1000]}개'
    
    @property
    def max_price(self) -> int:
        """
        재고가 있는 상품들 중 가장 높은 가격을 반환하는 프로퍼티

        Returns:
            int: 재고가 있는 상품들 중 가장 높은 가격
        """
        return max([i.price for i in self.products if i.count > 0])   # 재고가 있는 상품들 중 가장 높은 가격 반환
    
    @property
    def to_dict(self):
        return [product.to_dict for product in self.products]

    @property
    def products_name(self) -> list[Product]:
        """
        상품들의 이름을 리스트로 반환하는 프로퍼티
        """
        return [i.name for i in self.products] # 상품들의 이름을 리스트로 반환
    
    @property
    def products_id(self) -> list[int]:
        """ 
        상품들의 ID를 리스트로 반환하는 프로퍼티
        """
        return [i.id for i in self.products]
    
    @property
    def status(self) -> str:
        """
        자판기의 현재 상태를 문자열로 반환하는 프로퍼티

        Returns:
            str: 현재 투입된 금액을 포함한 상태 메시지
        """
        return f"투입된 금액 : {self.inserted_money}원\n"   # 현재 투입된 금액 반환


    def reset(self) -> None:
        """
        자판기를 초기화하는 메서드

        Returns:
            None
        """
        self.products: list[Product] = []   # 상품 리스트 초기화
        self.change_box: dict[int:int] = {100 : 100, 500 : 100, 1000 : 0}   # 거스름돈 보관함 초기화
        self.inserted_money: int = 0   # 투입된 금액 초기화
        self.user.reset()   # 사용자 정보 초기화
        return None
    
    def issue_report(self, issue_type : str = None, issue_on = None) -> None:
        """
        자판기 리포트를 작성하는 메서드
        
        Args:
            issue_type (str, optional): 리포트 이슈 타입. Defaults to None.
            issue_on (Product or int, optional): 리포트 이슈가 발생한 상품 혹은 금액. Defaults to None.
        
        Returns:
            None
            
        Raises:
            AssertionError
        
        """
        time = datetime.datetime.now()   # 현재 시간을 받아옴
        time_str = time.strftime('%Y/%m/%d-%H:%M:%S')   # 시간을 문자열로 변환
        # 리포트 파일을 열어서 이슈 타입에 따라 메시지 작성
        with open(self.report_file, 'a', encoding='utf-8') as f: 
            if issue_type == 'No_product': # 상품이 품절되었을 때
                assert type(issue_on) == Product # issue_on이 Product 클래스의 인스턴스인지 확인
                f.write(f'[{time_str}] {issue_on.id}. {issue_on.name} 상품의 재고가 없습니다.\n') # 리포트 파일에 메시지 작성
            elif issue_type == 'No_change': # 거스름돈이 부족할 때
                assert issue_on in ['100', '500', '1000'] # issue_on이 100, 500, 1000 중 하나인지 확인
                f.write(f'[{time_str}] {issue_on}원이 부족합니다.\n') # 리포트 파일에 메시지 작성
        return None
    
    def sort(self) -> list[Product]:
        """
        상품 리스트를 가격 기준으로 정렬하는 메서드

        Returns:
            list: 정렬된 상품 리스트
        """
        self.products.sort(key=int)   # 상품 리스트를 가격 기준으로 정렬
        return self.products   # 정렬된 상품 리스트 반환

    
    def add_product(self, name: str, price: int = None, count: int = 0, ID: int = None, product_type: str = None) -> list[Product]:
        """
        제품(Product)을 추가하는 메서드

        Args:
            name (str): 제품의 이름
            price (int, optional): 제품의 가격 (기본값: None)
            count (int, optional): 제품의 재고 수량 (기본값: 0)
            ID (int, optional): 제품의 고유 ID (기본값: None)
            product_type (str, optional): 제품의 종류 (기본값: None)

        Returns:
            list: 정렬된 상품 리스트
        """
        if type(name) is Product:
            self.products.append(name)   # 상품 객체가 인자로 전달되면 상품 리스트에 추가
        else:
            if not ID:
                ID = len(self.products) + 1   # ID가 주어지지 않으면 현재 상품 개수에 1을 더한 값으로 설정
            self.products.append(Product(ID=ID, name=name, price=price, count=count, product_type=product_type)) # 상품 리스트에 상품 객체 추가
        
        return self.sort()   # 상품 리스트를 정렬하여 반환

    
    def products_by_json(self) -> list[str]:
        """
        JSON 파일에서 제품 정보를 로드하여 제품을 추가하는 메서드
        
        Returns:
            List[str]: 추가된 제품들의 이름(name)을 담은 리스트
        """
        import json
        
        # JSON 파일을 열어 데이터를 로드합니다.
        with open(self.products_file, 'r', encoding='UTF-8') as f:
            json_data = json.load(f)
            
        # json_data를 순회하면서 제품(Product) 객체를 추가합니다.
        for i in json_data:
            # "id", "name", "price", "count" 값을 추출하여 제품 객체를 추가합니다.
            self.add_product(ID=int(i["id"]), name=i["name"], price=int(i["price"]), count=int(i["count"]))
        
        # 추가된 제품의 이름(name)들을 리스트로 반환합니다.
        return self.products_name
    
    def save_products(self):
        '''
        제품 정보를 JSON 파일에 저장하는 메서드
        '''
        import json
        
        with open(self.products_file,'w') as f:
            json.dump(self.to_dict, f)

    def delete_product(self, product: Product = None, id: int = None) -> list[Product]:
        """
        VendingMachine 클래스의 제품 삭제 메소드.
        
        Args:
            product (Product, optional): 삭제할 Product 객체. Defaults to None.
            id (int, optional): 삭제할 제품의 ID 값. Defaults to None.
            
        Returns:
            list: 제품이 삭제된 후의 제품 목록 (self.products)을 반환함.
            
        Raises:
            ValueError: product와 id 값이 모두 None인 경우 예외를 발생시킴.
        """
        if id is None and product is None:
            raise ValueError('Values are empty')  # product와 id 값이 모두 None인 경우 예외 발생

        for i in self.products:
            assert type(i) is Product  # self.products 리스트에 있는 객체들이 Product 클래스의 인스턴스인지 확인
            if i == product:
                self.products.remove(i)  # product 객체와 일치하는 제품을 삭제
                break
            elif i.id == id:
                self.products.remove(i)  # id 값과 일치하는 제품을 삭제
                break

        return self.products

    def edit_product(self, product: Product, name: str = None, price: int = None, count: int = None) -> Product:
        """
        VendingMachine 클래스의 제품 수정 메소드.
        
        Args:
            product (Product): 수정할 Product 객체.
            name (str, optional): 수정할 제품의 이름. Defaults to None.
            price (int, optional): 수정할 제품의 가격. Defaults to None.
            count (int, optional): 수정할 제품의 재고 수량. Defaults to None.
            
        Returns:
            Product: 수정된 Product 객체를 반환함.
            
        Raises:
            ValueError: product가 Product 클래스의 인스턴스가 아닌 경우 예외를 발생시킴.
        """
        assert type(product) is Product  # product가 Product 클래스의 인스턴스인지 확인
        property_list = {'name': name, 'price': price, 'count': count}
        
        for key, value in property_list.items():
            if value is not None:
                setattr(product, key, value)
                
        return product
    
    
    def insert_money(self, money: int) -> int:
        """
        투입한 돈을 자판기에 추가하는 메서드입니다.

        Args:
            money (int): 투입할 돈의 금액 (100, 500, 1000 중 하나)

        Returns:
            int: 현재까지 투입된 총 금액
        Raises:
            ValueError: 투입한 돈의 개수가 부족한 경우 예외 발생
            ValueError: 투입한 돈이 100, 500, 1000원 중 하나가 아닌 경우 예외 발생
        """
        if self.money_check(money=money):  # 투입한 돈이 100, 500, 1000원 중 하나인지 확인
            if self.user.money_box[money] < 1:
                raise ValueError('Not enough money')  # 투입한 돈의 개수가 부족한 경우 예외 발생
            self.user.money_box[money] -= 1  # 투입한 돈의 개수를 1 감소시킴
            self.change_box[money] += 1  # 자판기의 잔돈 상자에 투입한 돈의 개수를 1 증가시킴
            self.inserted_money += money  # 현재까지 투입된 총 금액을 업데이트
        else:
            raise ValueError('Wrong money')  # 투입한 돈이 100, 500, 1000원 중 하나가 아닌 경우 예외 발생
        return self.inserted_money  # 현재까지 투입된 총 금액 반환
    
    def refund(self, refund_dict: dict = {1000 : 0, 500 : 0, 100 : 0}) -> int:
        """
        사용자에게 환불을 처리하는 메소드

        Args:
            refund_dict (dict, optional): 환불할 거스름돈의 개수를 담은 딕셔너리. Defaults to {1000 : 0, 500 : 0, 100 : 0}.

        Returns:
            int: 환불된 총 금액
        """
        refund = 0
        for k, v in refund_dict.items():
            self.change_box[k] -= v   # 거스름돈 보관함에서 환불할 금액을 차감
            self.user.money_box[k] += v   # 사용자의 돈 보관함에 환불할 금액을 추가
            self.inserted_money -= k * v   # 투입된 금액에서 환불할 금액을 차감
            refund += k * v   # 총 환불 금액에 추가
        
        return refund_dict, refund   # 총 환불 금액 반환

    
    def cal_refund(self, product: Product = Product(ID=0, name='None', price=0, count=0)) -> dict[int, int]:
        """
        사용자에게 반환할 잔돈을 계산하고, 반환할 잔돈을 나타내는 딕셔너리를 반환하는 메서드입니다.

        Args:
            product (Product, optional): 반환할 제품 객체. 기본값은 None으로, None인 경우 자판기에 있는 None_product를 사용합니다.

        Returns:
            Dict[int, int]: 반환할 잔돈을 나타내는 딕셔너리. 키는 화폐 단위, 값은 개수로 나타내며, 잔돈이 없는 경우 빈 딕셔너리가 반환됩니다.

        Raises:
            ValueError: 자판기에 있는 잔돈이 부족한 경우 발생합니다.
        """

        # 거스름돈 계산에 사용할 변수들 초기화
        change_box = self.change_box.copy()  # 잔돈 보관함의 현재 상태를 복사하여 사용
        refund_dict = {500: 0, 100: 0}  # 거스름돈을 계산할 때 필요한 변수들
        sum_dict = sum([k * v for k, v in refund_dict.items()])  # refund_dict의 값을 합하여 초기화
        
        # 예상 잔돈 계산
        expected_balance = self.inserted_money - product.price - sum_dict
        
        # 입력된 돈이 0이 아니고, 예상 잔돈이 0보다 큰 동안 반복
        while self.inserted_money != 0 and expected_balance > 0:
            insufficient_change = 0  # 거스름돈 발생 여부를 확인하기 위한 변수
            for i in refund_dict:
                # 예상 잔돈이 i보다 크거나 같고, 해당 단위의 잔돈이 보관함에 남아있는 경우
                if self.inserted_money - product.price - sum_dict >= i: 
                    if change_box[i] > 0:
                        change_box[i] -= 1
                        refund_dict[i] += 1
                        sum_dict += i
                        expected_balance = self.inserted_money - product.price - sum_dict
                    else:
                        insufficient_change = i
            if insufficient_change: # 거스름돈이 부족한 경우
                for i in refund_dict: # 환불할 잔돈을 자판기의 잔돈 보관함에 다시 넣음
                    change_box[i] += refund_dict[i]
                    refund_dict[i] = 0
                raise ValueError(str(insufficient_change)) # 거스름돈이 부족한 단위를 반환
        return refund_dict # 환불할 잔돈을 나타내는 딕셔너리 반환

    def money_check(self,money:int = None,count:int = None):
        assert money in [1000, 500, 100, None], 'Wrong money'
        if money != None:
            assert count>0, 'Wrong count'
        
    def add_change(self, money: int, count: int) -> None:
        self.money_check(money,count)
        self.change_box[money] += count
        return count
    
    def get_change(self, money: int, count, int)-> None:
        self.money_check(money,count)

        change_count = min(count, self.change_box[money])
        self.change_box[money] -= change_count
        
        return change_count


    def buy(self, product_id: int) -> str:
        """
        상품을 구매하는 메소드

        Args:
            product_id (int): 상품의 ID

        Returns:
            str: 구매한 상품의 이름
        
        raises:
            ValueError: 구매가 불가능한 경우 발생
        """
        
        if product_id in self.products_id:   # 상품 ID가 존재하는 경우
            product:Product = self.products[product_id - 1]   # 상품 ID로부터 상품 객체를 가져옴
        else:
            raise ValueError('구매 불가능한 상품 ID')  # 상품 ID가 존재하지 않는 경우 예외 발생

        if self.is_sellable(product):   # 상품이 판매 가능한 상태인지 확인
            ouput = product.name   # 구매한 상품의 이름을 저장
            if self.user.is_credit:   # 사용자가 신용카드를 사용하는 경우
                self.user.credit_money -= product.price
            else:   # 현금으로 결제하는 경우
                refund_dict = self.cal_refund(product)   # 환불할 거스름돈 계산
                self.refund(refund_dict)   # 환불
                product.count -= 1   # 상품 수량 차감
                self.inserted_money -= product.price   # 투입된 금액에서 상품 가격 차감
                output += f' {self.inserted_money}원을 반환합니다.'   # 반환할 금액을 출력
            return ouput
        else:
            raise ValueError('구매 불가') # 구매 불가능한 경우 예외 처리
    
    def is_sellable(self, product: Product) -> bool:
        """
        상품을 구매할 수 있는지 확인하는 메서드
        
        Args:
            product (Product): 구매할 상품 객체
            
        Returns:
            bool: 구매 가능 여부
        """
        if product.is_empty: # 상품이 품절된 경우
            self.issue_report(issue_type='No_product',issue_on=product)
            return False
        # 신용카드를 사용하는 경우
        if self.user.is_credit:
            return self.user.credit_money >= product.price # 신용카드 잔액이 상품 가격보다 큰 경우 구매 가능
        
        # 현금을 사용하는 경우
        try:
            self.cal_refund(product)
        except ValueError as e: # 잔돈이 부족한 경우
            self.issue_report(issue_type="No_change", issue_on=str(e))
            return False
        return product.price <= self.inserted_money # 투입된 금액이 상품 가격보다 큰 경우 구매 가능
    