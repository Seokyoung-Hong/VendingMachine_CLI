import sys
import os
import platform
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


    def show_product(self, first=False) -> str:
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
            output = output + '\n' + product.product_info(self.machine, check_money=False)  # 상품 정보를 출력 메시지에 추가
        if first:
            end_output += '결제수단을 선택하세요.\n현금(cash) or 카드(card)\n'  # 첫 화면일 경우 결제수단 선택 메시지 추가
        else : 
            output += '상품을 구매하시려면 "구매 [상품 id]" 또는 "buy [상품 id]" 를 입력하세요\n'  # 상품 구매 메시지 추가
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

        Returns:
            str: 환불된 금액에 대한 메시지를 반환함
        """
        refund_dict: dict[int, int]
        refunded: int
        refund_dict, refunded = self.machine.refund(self.machine.cal_refund())  # 환불할 금액 계산 후 자판기에 환불 요청
        return ''.join(f'{k}원 {v}개, ' for k,v in refund_dict.items())+'\n'+f"{refunded}원 환불되었습니다.\n"  # 환불된 금액에 대한 메시지 반환

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
            output = f'{self.machine.buy(product_id=Input)} 구매 완료\n'  # self.machine의 buy 메서드를 호출하여 상품을 구매하고 출력 메시지 설정
        except ValueError as e:
            if str(e) == '구매 불가':
                output = '구매 불가\n'  # 상품 구매가 불가능한 경우 오류 메시지 설정
            elif str(e) == '구매 불가능한 상품 ID':
                output = '구매 불가능한 상품 ID\n'  # 상품 ID가 존재하지 않는 경우 오류 메시지 설정
            
        return ('', output)  # 빈 문자열과 output을 튜플로 반환

    
    def insert(self, money: int) -> tuple:
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
        except ValueError as e:
            if str(e) == 'Not enough money':
                end_output = '해당 화폐를 가지고 있지 않습니다.\n'  # 돈이 충분하지 않을 경우 오류 메시지 설정
            elif str(e) == 'Wrong money':
                end_output = '동전을 다시 투입해주세요.\n'  # 잘못된 화폐를 투입한 경우 오류 메시지 설정
            else:
                raise ValueError(e)

        else:
            end_output = f'{money}원이 투입되었습니다.\n\n'  # money가 정상적으로 투입된 경우 메시지 설정

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
        elif Input.isdigit() and not self.is_credit:
            return self.reload(self.insert(money=int(Input)))  # 숫자로 시작하는 입력에 대한 처리
        elif Input in ['exit', '나가기']:
            raise SystemExit  # exit 명령어 처리
        return Input  # 그 외의 입력은 그대로 반환


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
        # output이 튜플인 경우 output과 end_output으로 분리
        if type(output) == tuple:
            output, end_output = output
        
        # 화면을 클리어하여 리로드
        if platform.platform().startswith('Windows'): # Windows 운영체제인 경우
            os.system('cls')  
        else: # 그 외의 운영체제인 경우
            os.system('clear')
        
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