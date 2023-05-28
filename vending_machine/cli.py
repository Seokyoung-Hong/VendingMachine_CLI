import platform
import sys
import os
import hashlib
from .vendingmachine import VendingMachine, Product

__all__ = ['CommandLineInterface']

class CommandLineInterface(BaseException):
    def __init__(self, VM: VendingMachine) -> None:
        """
        커맨드 라인 인터페이스(Command Line Interface)를 나타내는 클래스

        Args:
            VM (VendingMachine): 자판기(VendingMachine) 객체
        """
        self.machine = VM
        self.password_file = 'passwd.txt'

    @property
    def is_credit(self) -> bool:
        """
        카드 모드인지 여부를 반환하는 속성

        Returns:
            bool: 사용자의 카드모드 여부 (True: 카드 모드, False: 현금 모드 )
        """
        return self.machine.user.is_credit

    @property
    def status(self) -> str:
        """
        사용자의 상태와 자판기의 상태를 반환하는 속성

        Returns:
            str: 사용자의 상태와 자판기의 상태를 문자열로 반환
        """
        if self.is_credit:
            return f'{self.machine.user.status}\n'
        return f'{self.machine.user.status}\n{self.machine.status}\n'

    def clear(self) -> None:
        """
        화면을 지우는 메서드
        """
        if platform.platform().startswith('Windows'): # Windows 운영체제인 경우
            os.system('cls')  
        else: # 그 외의 운영체제인 경우
            os.system('clear')

    def pay_method(self, Input) -> str:
        """
        결제 수단을 변경하는 메서드

        Args:
            Input (str): 변경할 결제 수단

        Returns:
            str: 변경된 결제 수단에 대한 메시지를 반환
        """
        output = ''
        if Input in ['카드', 'card']:
            self.machine.user.is_credit = True  # 사용자의 결제 수단을 카드로 변경
            output += '결제수단을 카드로 변경했습니다.\n'  # 변경된 결제 수단에 대한 메시지 추가
        elif Input in ['현금', 'cash']:
            output += '결제수단을 현금으로 변경했습니다.\n'  # 변경된 결제 수단에 대한 메시지 추가
        return output


    def show_product(self, first=False, manage=False) -> str:
        """
        물품 목록을 보여주는 메서드

        Args:
            first (bool, optional): 첫 화면인지 여부를 나타내는 플래그. 기본값은 False.

        Returns:
            str: 물품 목록과 관련된 메시지를 반환
        """
        products: list = self.machine.products  # 자판기의 상품 목록을 가져옴
        output = '물품 목록\n'  # 출력할 물품 목록 메시지 초기화
        end_output = ''
        for product in products:
            assert type(product) is Product  # Product 객체인지 확인
            output = output + '\n' + product.product_info(self.machine, check_money=False, manage_mod=manage)  # 상품 정보를 출력 메시지에 추가
        if first:
            end_output += '결제수단을 선택하세요.\n현금(cash) or 카드(card)\n'  # 첫 화면일 경우 결제수단 선택 메시지 추가
        elif not manage:
            output += '\n\n상품을 구매하시려면 "구매 [상품 id]" 또는 "buy [상품 id]" 를 입력하세요\n'  # 상품 구매 메시지 추가
        return (output,end_output)  # 최종적으로 구성된 메시지 반환



    @property
    def buyable_product(self) -> str:
        """
        구매 가능한 물품 목록을 반환하는 프로퍼티

        Returns:
            str: 구매 가능한 물품 목록과 관련된 메시지를 반환
        """
        products: list = self.machine.products  # 자판기의 상품 목록 가져오기
        t_output = '구매 가능한 물품 목록\n'  # 출력할 메시지의 시작 부분
        output = ''  # 출력할 메시지

        # 상품 목록을 순회하며 구매 가능한 상품인 경우 출력할 메시지에 추가
        for product in products:
            assert type(product) is Product  # 상품 객체인지 확인
            if self.machine.is_sellable(product):  # 자판기에서 판매 가능한 상품인지 확인
                output = output + '\n' + product.product_info(self.machine)  # 상품 정보를 메시지에 추가

        if len(output) == 0:
            output = '구매 가능한 물품이 없습니다. 금액을 투입하거나, 재고를 확인해주세요'
        else:
            output = t_output + output

        output += '\n\n'  # 메시지의 끝 부분에 개행 추가
        return output  # 최종적으로 구성된 메시지 반환

    @property
    def help(self) -> str:
        return """
자판기 프로그램 사용 설명서입니다.
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
1. 지불 방법 선택
    ├─현금 cash: 동전이나 지폐를 자판기에 투입해 물품을 구매합니다.
    └─카드 card: 현금 투입 없이, 판매중인 물품중 최고 금액을 투입합니다. 이후 현금 사용은 불가능합니다.

2. 지불
    ├─현금 : 100원을 투입하시려면 100을 입력하세요. (100원, 500원, 1000원만 투입 가능)
    └─카드 : 입력 없이 자동으로 잔고가 감소합니다.

3. 구매
    └─ 원하는 상품의 ID를 입력하세요.

명령어 목록
    ├─help 도움: 프로그램 사용 설명서를 보여줍니다.
    ├─list 목록 : 물품의 모든목록을 보여줍니다.
    ├─buyable 구매가능목록 : 현재 구매 가능한 물품의 목록을 보여줍니다.
                            다음 단계가 정해지지 않은 경우, 명령어를 입력하지 않았을 때에도 본 목록이 보여집니다.
    ├─100 500 1000 : 해당되는 금액을 자판기에 투입합니다.
    ├─refund 환불 : 투입한 금액을 환불받습니다.
    └─exit 나가기 : 자판기 프로그램을 종료합니다.

└────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

계속하시려면 아무 키나 누르세요
"""

    def refund(self) -> str:
        """
        자판기에 투입한 금액을 환불하는 메서드
.
        Returns:
            str: 환불된 금액에 대한 메시지를 반환함
        """
        refund_dict: dict[int, int]
        refunded: int
        refund_dict, refunded = self.machine.refund(self.machine.cal_refund())  # 환불할 금액 계산 후 자판기에 환불 요청
        return ''.join(f'{k}원 {v}개 ' for k,v in refund_dict.items())+'\n'+f"{refunded}원 환불되었습니다.\n"  # 환불된 금액에 대한 메시지 반환

    def buy(self, Input: str) -> tuple:
        """
        상품을 구매하는 메서드입니다.

        Args:
            Input (str): 상품 ID 입력 문자열 (예: "구매 [상품 id]" 또는 "buy [상품 id]")

        Returns:
            tuple: (빈 문자열, 구매 완료 메시지) 또는 (빈 문자열, 구매 불가 메시지)
        """
        Input = Input.replace('buy ', '')  # Input에서 "buy "를 제거하여 상품 ID만 추출
        Input = int(Input.replace('구매 ', ''))  # Input에서 "구매 "를 제거하여 상품 ID만 추출하고 정수로 변환

        try:
            product_name, refund_dict = self.machine.buy(product_id=Input) # 상품 구매
            output = f'{product_name} 구매 완료\n' # 구매 완료 메시지 설정
            if refund_dict is not None: # 환불된 금액이 있는 경우
                 output += ''.join(f'{k}원 {v}개, ' for k,v in refund_dict.items())+"환불되었습니다.\n" # 환불된 금액에 대한 메시지 설정
        except ValueError as e:
            if str(e) == '구매 불가':
                output = '구매 불가\n'  # 상품 구매가 불가능한 경우 오류 메시지 설정
            elif str(e) == '구매 불가능한 상품 ID':
                output = '구매 불가능한 상품 ID\n'  # 상품 ID가 존재하지 않는 경우 오류 메시지 설정
            
        return ('', output)  # 빈 문자열과 output을 튜플로 반환

    
    def insert(self, money: int) -> tuple[str, str]:
        """
        돈을 투입하는 함수입니다.

        Args:
            money (int): 투입할 돈의 금액

        Returns:
            tuple: (output, end_output) 형태의 튜플로 반환됩니다.
                - output: 출력 메시지 문자열
                - end_output: 마지막 출력 메시지 문자열
        
        Raises:
            ValueError: money가 100, 500, 1000이 아닌 경우
        """
        output = ''
        end_output = None
        try:
            self.machine.insert_money(money=money)  # money를 self.machine에 삽입
            end_output = f'{money}원이 투입되었습니다.\n\n'  # money가 정상적으로 투입된 경우 메시지 설정
        except ValueError as e:
            if str(e) == 'Not enough money':
                end_output = '해당 화폐를 가지고 있지 않습니다.\n'  # 돈이 충분하지 않을 경우 오류 메시지 설정
            elif str(e) == 'Wrong money':
                end_output = '동전을 다시 투입해주세요.\n'  # 잘못된 화폐를 투입한 경우 오류 메시지 설정
            else:
                raise ValueError(e)

        finally:
            output = output + self.buyable_product + '\n\n'  # self.buyable_product를 output에 추가
            return (output, end_output)  # output과 end_output 반환


    def chk_cmd(self, Input: str) -> str:
        """
        사용자 입력을 검사하고 해당하는 명령을 실행하는 메서드입니다.

        Args:
            Input (str): 사용자 입력 문자열

        Returns:
            str: 출력 메시지 문자열
        
        Raises:
            SystemExit: 사용자 입력이 "exit" 또는 "나가기"인 경우
        """
        if Input in ["help", "도움"]:
            return self.reload(self.help)  # help 명령어 처리
        elif Input in ["list", "목록"]:
            return self.reload(self.show_product())  # list 명령어 처리
        elif Input in ["buyable", "구매가능목록"]:
            return self.reload(self.buyable_product)  # buyable 명령어 처리
        elif Input in ["refund", "환불"]:
            return self.reload(self.refund())  # refund 명령어 처리
        elif Input.startswith(('buy ','구매 ')) and (Input[3:].isdigit() or Input[4:].isdigit()):
            return self.reload(self.buy(Input))  # buy 명령어 처리
        elif Input.strip().isdigit() and not self.is_credit:
            return self.reload(self.insert(money=int(Input)))  # 숫자로 시작하는 입력에 대한 처리
        elif Input in ['management','관리자']: # 관리자 모드 진입
            return self.reload(self.management())
        elif Input in ['exit', '나가기']:
            raise SystemExit  # exit 명령어 처리
        
        return Input  # 그 외의 입력은 그대로 반환

    def check_passwd(self) -> bool:
        """
        비밀번호를 확인하는 메서드입니다.
        
        Returns:
            bool: 비밀번호가 일치하는 경우 True, 그렇지 않은 경우 False를 반환
        """
        if os.path.exists(self.password_file):
            before_passwd = input('비밀번호를 입력하세요: ')
            m = hashlib.sha256()
            m.update(before_passwd.encode('utf-8'))
            with open(self.password_file, 'r') as f:
                return m.hexdigest() == f.read()
        else:
            self.change_passwd()
            return True
    
    def change_passwd(self):
        """
        비밀번호를 변경하는 메서드입니다.
        
        Returns:
            str: 비밀번호 변경 완료 메시지를 반환
        """
        self.clear()
        passwd = input('새로운 비밀번호를 입력하세요:')
        with open('passwd.txt', 'w') as f:
            m = hashlib.sha256()
            m.update(passwd.encode('utf-8'))
            f.write(m.hexdigest())
        return '나가기'

    def add_product(self):
        """
        상품을 추가하는 메서드입니다.
        
        Returns:
            str: 상품 추가 완료 메시지를 반환
        """
        name = input('추가할 상품의 이름을 입력하세요: ')
        try:
            price = int(input('추가할 상품의 가격을 입력하세요: '))
        except ValueError:
            print('잘못된 입력입니다. 다시 입력해주세요.')
            return self.add_product()
            
        try :
            count = int(input('추가할 상품의 개수를 입력하세요(미입력시 30): '))
        except ValueError:
            count = 30
        
        self.machine.add_product(name=name,price=price,count=count)
        return '나가기'
    
    def select_product(self, action: str):
        """
        상품을 선택하는 메서드입니다.
        
        Args:
            action (str): 수행할 동작을 나타내는 문자열
        
        Returns:
            Product: 선택된 상품(Product) 객체
        """
        sys.stdout.write(self.show_product(manage=True)[0]+'\n')
        while True:
            id = int(input(f'{action}할 상품의 번호를 입력하세요: '))
            for product in self.machine.products:
                if product.id == id:
                    return product
            self.clear()
            print('잘못된 상품 번호입니다. 다시 입력해주세요.')

    def delete_product(self):
        """
        상품을 삭제하는 메서드입니다.
        
        Returns:
            str: 상품 삭제 완료 메시지를 반환
        """
        product = self.select_product('삭제')
        if product:
            self.machine.delete_product(product)
            resort = input('상품을 삭제하였습니다. 상품 ID를 재정렬하시겠습니까?(y/n): ')
            if resort == 'y':
                self.machine.resort_product()
                sys.stdout.write("상품 ID를 재정렬하였습니다.\n")
        return '나가기'


    
    def edit_product(self):
        """
        상품을 수정하는 메서드입니다.
        
        Returns:
            str: 상품 수정 완료 메시지를 반환
        """
        if len(self.machine.products) == 0:
            self.clear()
            print('자판기에 상품이 존재하지 않습니다.')
            return None
        target_product = self.select_product('수정')
        
        name = input('수정할 상품의 이름을 입력하세요(미입력시 미수정): ').strip() or None
        price = input('수정할 상품의 가격을 입력하세요(미입력시 미수정): ').strip() or None
        count = input('수정할 상품의 개수를 입력하세요(미입력시 미수정): ').strip() or None

        self.machine.edit_product(name=name,price=price,count=int(count),product=target_product)
        return '상품수정 완료'
    
    def edit_products(self):
        """
        상품을 수정하는 메서드입니다.
        
        Returns:   
            str: 상품 수정 완료 메시지를 반환
        """
        functions = [self.add_product, self.delete_product, self.edit_product, lambda: '나가기']
        self.clear()
        try:
            Input = int(input('1. 상품 추가\n2. 상품 삭제\n3. 상품 수정\n4. 나가기\n'))
            return functions[Input-1]()
        except:
            print('잘못된 입력입니다.')
            return self.edit_products()
    
    def edit_change(self):
        """
        잔돈을 수정하는 메서드입니다.
        
        Returns:
            str: 잔돈 수정 완료 메시지를 반환
        """
        self.clear()
        sys.stdout.write(self.machine.change_box_info)
        try :
            Input = int(input('1. 잔돈 추가\n2. 잔돈 인출\n3. 나가기\n'))
            functions = [self.add_change, self.get_change, lambda: '나가기']
            return functions[Input-1]()
        except:
            print('잘못된 입력입니다.')
            return self.edit_change()
    
    def add_change(self):
        """
        잔돈을 추가하는 메서드입니다.
        
        Returns:
            str: 잔돈 추가 완료 메시지를 반환
        """
        self.clear()
        try:
            money = int(input('추가할 잔돈의 종류를 입력하세요: '))
            count = int(input('추가할 잔돈의 개수를 입력하세요: '))
            count = self.machine.add_change(money=money, count=count)
            return f'{money}원 {count}개 추가 완료'
        except:
            print('잘못된 입력입니다.')
            return self.add_change()
    
    def get_change(self):
        """
        잔돈을 인출하는 메서드입니다.
        
        Returns:
            str: 잔돈 인출 완료 메시지를 반환
        
        Raises:
            Exception: 잔돈이 부족하거나 입력이 잘못된 경우
        """
        try:
            money = int(input('인출할 잔돈의 종류을 입력하세요: '))
            count = int(input('인출할 잔돈의 개수를 입력하세요: '))
            real_count =  self.machine.get_change(money=money,count=count)
            return f'{money}원 {real_count}개 인출 완료'
        except Exception as e:
            self.clear()
            if str(e) == 'Not enough change':
                print('잔돈이 부족합니다.')
            else:
                print('잘못된 입력입니다.')
            return self.get_change()
    
    
    def management(self):
        """
        관리자 모드를 실행하는 메서드입니다.
        
        Returns:
            str: 관리자 모드 종료 메시지를 반환
        """
        if self.check_passwd():
            options = {
                '1': self.edit_products,
                '2': self.edit_change,
                '3': self.change_passwd,
                '4': lambda: '나가기',
            }
            while True:
                input_text = input('관리자 모드입니다. 실행하고 싶은 기능의 숫자를 입력하세요.\n1. 상품 수정\n2. 잔돈 수정\n3. 비밀번호 변경\n4. 나가기\n')
                if input_text in options:
                    result = options[input_text]()
                    if any(word in result for word in  ['나가기', '완료']) :
                        break
                else:
                    self.clear()
                    print('잘못된 입력입니다.')
        else:
            print("비밀번호가 일치하지 않습니다.")
        return f'\n{result}\n관리자 모드 종료'


    def reload(self, output='', end_output='', product_list=True):
        """
        화면을 리로드하고 출력할 내용을 출력하고 사용자 입력을 받아 해당 명령을 실행하는 메서드입니다.

        Args:
            output (str, optional): 출력할 내용의 시작 부분. 기본값은 빈 문자열입니다.
            end_output (str, optional): 출력할 내용의 끝 부분. 기본값은 빈 문자열입니다.
            product_list (bool, optional): 상품 목록을 출력할 지 여부를 결정하는 플래그입니다. 
                기본값은 True로 상품 목록을 출력합니다.

        Returns:
            str: 출력 메시지 문자열
        """
        self.machine.chk_everytime()
        # output이 튜플인 경우 output과 end_output으로 분리
        if type(output) == tuple:
            output, end_output = output
        
        self.clear()  # 화면 리로드
        
        if output is not None:
            sys.stdout.write(output)  # 출력할 내용의 시작 부분 출력
        if self.is_credit and product_list:
            sys.stdout.write(self.buyable_product+'\n')  # 상품 목록 출력
        sys.stdout.write('\n'+self.status)  # 현재 상태 출력
        if end_output is not None:
            sys.stdout.write(end_output+'\n')  # 출력할 내용의 끝 부분 출력
        Input = input('>>>')  # 사용자 입력 받기
        return self.chk_cmd(Input)  # 입력된 명령어 처리


    def run(self) -> None:
        """
        자판기를 실행하는 메서드입니다. 초기 화면을 로드하고 사용자 입력을 받아 명령을 처리하며, 무한 루프에서 실행됩니다.
        """
        self.reload(self.help)  # 초기 화면 로드
        Input = self.reload(self.show_product(first=True))  # 상품 목록 및 결제 방법 출력
        Input = self.reload(self.pay_method(Input=Input))  # 결제 방법 선택
        while True:
            self.reload(self.chk_cmd(Input))  # 사용자 입력에 따른 명령어 처리
