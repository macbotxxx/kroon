from decimal import Decimal
from kroon_token.models import PurchaseTokenFees






class Transactional_Percentage:
    """
    Transactional percentage is been calculated before any transaction going through
    ether through kroon wallet or withdraw transaction.
    """

    def kroon_transfer_percentage(self , request , *args, **kwargs):
        
        """
        kroon transfer percentage is calculated during a transfer between 
        kroon customers and in the same country NOTE: international transaction
        is not allowed at the moment.
        
        """
        amount = kwargs.get("amount")

        # getting the users country transfer rate
        users_country = PurchaseTokenFees.objects.get( country = request.user.country_of_residence.id )
        rate = users_country.kroon_transfer_rate
    
        fees = ( Decimal(amount) * rate ) / 100
        # vat_fees = ( amount * percentage ) / 100
        # total_vat_fee = format(vat_fees, '.2f')
        rate_fee = format(fees, '.2f')
        final_amount = Decimal(amount) - Decimal (rate_fee)
        
        return final_amount 


    def virtual_card_percentage( self, request, *args, **kwargs):
        pass


    



