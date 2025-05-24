import random
from datetime import datetime

from account.models import User


class Generate_Username:

    def __init__(self, first_name, last_name, birth_date):
        self.special_chars = ['', '_', '.', '-']
        random.shuffle(self.special_chars)
        self.d_obj = datetime.strptime(birth_date, "%Y-%m-%d")
        self.first_name = first_name
        self.last_name = last_name
    
    def _find_available_name(self, combinations):
        """
        Helper method that checks a list of username combinations against the database
        and returns the first available one.
        
        Args:
            combinations: List of possible username combinations to check
            
        Returns:
            The first available username, or empty string if none are available
        """
        existing_usernames = set(User.objects.filter(username__in=combinations)
                                .values_list('username', flat=True))
        
        for name in combinations:
            if name not in existing_usernames:
                return name
                
        return ""
    
    def f_sp_l(self) -> str:
        """
        Trying `[First name][Special Character][Last name]`\n
        returns "*generated_username*" if successful, else returns empty string ""\n
        T(n) = 4n
        """
        combinations = [f"{self.first_name}{sp}{self.last_name}" for sp in self.special_chars]
        return self._find_available_name(combinations)
    
    def f_sp_l_sp(self) -> str:
        """
        Trying `[First name][Special Character][Last name][Special Character]`\n
        returns "*generated_username*" if successful, else returns empty string ""\n
        T(n) = 4n * 4n = 16n
        """
        combinations = [
            f"{self.first_name}{sp_1}{self.last_name}{sp_2}" 
            for sp_1 in self.special_chars 
            for sp_2 in self.special_chars
        ]

        return self._find_available_name(combinations)
    
    def f_sp_l_sp_bd(self):
        """
        Trying `[First name][Special Character][Last name][Special char][Birth date]`\n
        returns "*generated_username*" if successful, else returns empty string ""\n
        T(n) = 4n * 4n = 16n
        """
        combinations = [
            f"{self.first_name}{sp_1}{self.last_name}{sp_2}{self.d_obj.day}" 
            for sp_1 in self.special_chars 
            for sp_2 in self.special_chars
        ]

        return self._find_available_name(combinations)
    
    def sp_f_sp_l_sp_bd(self):
        """
        Trying `[Special Char][First name][Special Character][Last name][Special char][Birth date]`\n
        returns "*generated_username*" if successful, else returns empty string ""\n
        T(n) = 4n * 4n * 4n = 64n (maximum)
        """

        combinations = [
            f"{sp_1}{self.first_name}{sp_2}{self.last_name}{sp_3}{self.d_obj.day}"
            for sp_1 in self.special_chars
            for sp_2 in self.special_chars
            for sp_3 in self.special_chars
        ]
        
        # Due to potentially large number of combinations, I am just batching them
        batch_size = 50
        for i in range(0, len(combinations), batch_size):
            batch = combinations[i:i+batch_size]
            result = self._find_available_name(batch)
            if result:
                return result
                
        return ""

    def generate_unique_name(self) -> str:
        # Now just calling these functions using for loop
        for method in [self.f_sp_l, self.f_sp_l_sp, self.f_sp_l_sp_bd, self.sp_f_sp_l_sp_bd]:
            result = method()
            if result:
                return result
                
        return "can't suggest name for now"