import unicodedata


__all__ = ['TextFormatter']

class TextFormatter:
    @staticmethod
    def textColor(text: str, color: str, bg=False) -> str:
        """
        텍스트의 색상을 변경하는 함수.
        
        Args:
            text (str): 변경할 텍스트
            color (str): 변경할 색상 ('black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white', 'default' 중 하나)
            bg (bool): 배경색을 변경할지 여부 (True면 배경색, False면 글자색)
        
        Returns:
            str: 변경된 텍스트
        """
        col_list = ['black', 'red', 'green', 'yellow',
                    'blue', 'magenta', 'cyan', 'white', None, 'default']
        if color == 'reset':
            return '\033[0m'  # ANSI 코드를 사용하여 텍스트의 색상을 리셋하는 코드
        # ANSI 코드를 사용하여 텍스트의 색상을 변경하는 코드. color와 bg에 따라 적절한 코드를 생성하여 반환함.
        return f'\033[{col_list.index(color) + (40 if bg else 30)}m' + text + '\033[0m'

    @staticmethod
    def fill_str_with_space(input_s: str, max_size: int = 28, fill_char=" ") -> str:
        """
        주어진 문자열을 주어진 최대 크기로 채우기 위해 공백 문자를 추가하는 함수.
        
        Args:
            input_s (str): 입력 문자열
            max_size (int): 최대 크기
            fill_char (str): 채울 문자
        
        Returns:
            str: 최대 크기로 채워진 문자열
        """
        l = 0
        # 입력된 문자열의 폭을 계산함
        for c in input_s:
            if unicodedata.east_asian_width(c) in ['F', 'W']:
                l += 2  # 동아시아 폭(Wide, Fullwidth)인 경우 2를 더함
            else:
                l += 1  # 그 외의 경우 1을 더함
        return input_s + fill_char * (max_size - l)  # 입력된 문자열을 주어진 최대 크기로 채우기 위해 fill_char를 사용함
