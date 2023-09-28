from django.db import models
from kroon.users.models import User, BusinessProfile
from django.utils.translation import gettext_lazy as _
from helpers.common.basemodel import BaseModel
from locations.models import Country




class Business_Agreements(BaseModel):
    """
    A business agreement refers to a legally binding contract or arrangement between two or more parties who engage in a business relationship. It outlines the terms and conditions that govern their interactions, rights, and obligations with regards to a specific business transaction or ongoing business activities.

    Business agreements can take various forms depending on the nature of the relationship and the purpose of the agreement. They can include contracts, partnership agreements, joint venture agreements, licensing agreements, franchise agreements, supply agreements, and many others.

    The agreement typically includes provisions related to the scope of work, responsibilities of each party, payment terms, delivery schedules, intellectual property rights, confidentiality, dispute resolution mechanisms, termination conditions, and other relevant terms and conditions.

    A well-drafted business agreement helps establish clear expectations and protects the interests of all parties involved, ensuring that they understand their rights and obligations. It provides a framework for conducting business in a structured and legally enforceable manner.
    """

    document = models.CharField(
        verbose_name=_("Document Name"),
        max_length = 200,
        blank=True,
        null=True, 
        help_text=_("this hold the document file name")

    )

    document_thumbnail = models.ImageField(
        verbose_name=_("Document Thumbnail"),
        upload_to="business_document",
        blank=True,
        null=True, 
        help_text=_("this hold the document file which is downloadable by the merchants ")
    )

    document_file = models.FileField(
        verbose_name=_("Document File"),
        upload_to="business_document_file",
        blank=True,
        null=True, 
        help_text=_("this hold the document file which can be in any format")
    )

    active = models.BooleanField(
        verbose_name=_('Document Available'),
        default = True,
        null=True, 
        blank=True,
        help_text=_("this indicates whether the document is available or not")
    )

    def __str__(self):
        return str(self.document)
    
    class Meta:
        ordering = ('-created_date',)
        verbose_name = _('Business Document')
        verbose_name_plural = _('Business Document')


class Agreements_Info(BaseModel):
    """
    Agreement information typically refers to the details and specifics contained within a particular agreement. It encompasses the relevant information, terms, conditions, and provisions outlined in the agreement that define the rights, responsibilities, and obligations of the parties involved.
    """

    user = models.ForeignKey(
        User,
        verbose_name=_("User Account"),
        on_delete=models.CASCADE, null=True,
        related_name="agreement_owner",
        blank=True,
        help_text=_("The user associated with this business agreement.")
    )

    business_name = models.CharField(
        verbose_name=_("Business Name"),
        max_length = 200,
        null=True, 
        help_text=_("A business name refers to the official name by which the company, organization, or sole proprietor operates and conducts its business activities. It is the name under which a business is registered and recognized legally.")
    )

    industry = models.CharField(
        verbose_name=_("Industry"),
        max_length = 200,
        null=True, 
        help_text=_("The industry in which the business operates.")
    )

    business_logo = models.ImageField(
        verbose_name=_("Business Logo"),
        upload_to="business_document",
        null=True, 
        help_text=_("A business logo is a graphic or symbol that represents a company or brand. It is a visual representation of the business and plays a crucial role in establishing brand identity and recognition")
    )

    business_owner_name = models.CharField(
        verbose_name=_("Business Owner Name"),
        max_length = 200,
        null=True, 
        help_text=_("A business name refers to the official name by which a company, organization, or sole proprietor operates and conducts its business activities. It is the name under which a business is registered and recognized legally.")
    )

    business_address = models.CharField(
        verbose_name=_("Business Address"),
        max_length = 200,
        null=True, 
        help_text=_("The business address refers to the physical location where a business is located or operates from. It serves as the specific street address, city, state, and postal code that uniquely identifies the business's place of operation.")
    )

    business_country  = models.CharField(
        verbose_name=_("Business Country"),
        max_length = 200,
        null=True, 
        help_text=_("The business Country in which the business operates.")
    )
    
    employee_name = models.CharField(
        verbose_name=_("Employee Name"),
        max_length = 200,
        null=True, 
        help_text=_("An employee name refers to the personal name given to an individual who is employed by a company or organization")
    )

    employee_address = models.CharField(
        verbose_name=_("Employee Address"),
        max_length = 200,
        null=True, 
        help_text=_("The term employee address refers to the residential address or location where an employee resides. It is the physical address where an employee lives and is used for communication and administrative purposes by the employer.")
    )

    employee_position = models.CharField(
        verbose_name=_("Employee Position"),
        max_length = 200,
        null=True, 
        help_text=_("An employee position refers to the specific role or job title held by an individual within an organization. It signifies the responsibilities, duties, and level of authority associated with that particular role. ")
    )

    employee_start_date = models.CharField(
        verbose_name=_("Employee Start Date"), 
        null=True,
        blank=True,
        max_length=100,
        help_text=_("The date when the employee started working.")
        )
    
    employment_term = models.CharField(
        verbose_name=_("Employment Term"), 
        max_length=100,
        null=True, 
        help_text=_("The term or duration of the employment agreement.")
        )
    
    employee_end_date = models.CharField(
        verbose_name="Employee End Date", 
        null=True,  
        blank=True,
        max_length=100,
        help_text=_("The date when the employee's employment ends, if applicable.")
        )
    
    employee_salary = models.CharField(
        max_length=100, 
        blank=True,
        null=True,  
        verbose_name="Employee Salary", 
        help_text=_("The salary of the employee.")
        )
    
    payment_frequency = models.CharField(
        verbose_name="Payment Frequency", 
        max_length=100, 
        null=True, 
        help_text=_("The frequency at which the employee is paid.")
        )
    
    employee_responsibilities = models.TextField(
        verbose_name="Employee Responsibilities", 
        help_text=_("The responsibilities and duties of the employee.")
        )
    
    weekly_hours = models.CharField(
        verbose_name="Weekly Hours", 
        null=True, 
        max_length = 200,
        blank = True, 
        help_text=_("The number of hours the employee is expected to work per week.")
        )
    
    travel_required = models.BooleanField(
        verbose_name="Travel Required",
        null=True, 
        default = False, 
        help_text=_("Indicates whether travel is required for the employee.")
        )
    
    company_policies = models.TextField(
        verbose_name="Company Policies", 
        help_text=_("The policies and guidelines of the company.")
        )
    
    employee_signature = models.ImageField(
        verbose_name=_("Employee Signature"),
        upload_to="signatures",
        null=True, 
        blank=True,
        help_text=_("A business logo is a graphic or symbol that represents a company or brand. It is a visual representation of the business and plays a crucial role in establishing brand identity and recognition")
    )

    signature = models.ImageField(
        verbose_name=_(" Signature"),
        upload_to="signatures",
        null=True, 
        blank=True,
        help_text=_("A business logo is a graphic or symbol that represents a company or brand. It is a visual representation of the business and plays a crucial role in establishing brand identity and recognition")
    )

    formatted_date = models.CharField(
        verbose_name=_("Formatted Date"), 
        null=True, 
        max_length = 200,
        blank=True,
        help_text=_("The date is formatted to when the agreement is taken.")
        )
    
    

    def __str__(self):
        return str(self.user)
    
    class Meta:
        ordering = ('-created_date',)
        verbose_name = _('Agreement info')
        verbose_name_plural = _('Agreement info')
    

class Shares_Signatures (BaseModel):
    """
    this holds the signatures of the share holders
    """
    agreements = models.ForeignKey(
        'Shares_Agreements',
        verbose_name=_("Shares Agreements"),
        on_delete=models.CASCADE, null=True,
        related_name="agreements_docs",
        blank=True,
        help_text=_("The agreements assocaited to the documents.")
    )

    name = models.CharField(
        verbose_name=_("Name"),
        max_length = 200,
        null=True, 
        help_text=_("this represents the name of the person.")
    )

    address = models.CharField(
        verbose_name=_("Address"),
        max_length = 200,
        null=True, 
        help_text=_("this represents the name of the person.")
    )

    share = models.CharField(
        verbose_name=_("Share"), 
        null=True, 
        max_length = 200,
        help_text=_("The number of hours the employee is expected to work per week.")
        )

    share_price = models.CharField(
        verbose_name=_("Share Price"),
        null=True,  
        max_length = 200,
        blank=True, 
        help_text=_("The salary of the employee.")
        )
    
    shares_signature = models.ImageField(
        verbose_name=_("Shares Signature"),
        upload_to="shares_signatures",
        blank=True,
        null=True, 
        help_text=_("A business logo is a graphic or symbol that represents a company or brand. It is a visual representation of the business and plays a crucial role in establishing brand identity and recognition")
    )
    

    def __str__(self):
        return str(self.name)
    
    class Meta:
        ordering = ('-created_date',)
        verbose_name = _('Shares Signature')
        verbose_name_plural = _('Shares Signature') 



class Shares_Agreements (BaseModel):
    """
    this holds the share agreements 
    """

    user = models.ForeignKey(
        User,
        verbose_name=_("User Accounts"),
        on_delete=models.CASCADE, null=True,
        related_name="agreement_owner_SA",
        blank=True,
        help_text=_("The user associated with this business agreement.")
    )

    company_name = models.CharField(
        verbose_name=_("Company Name"),
        max_length = 200,
        null=True, 
        help_text=_("this represents the name of the company that is issuring the shares.")
    )

    company_country = models.CharField(
        verbose_name=_("Company Country"),
        max_length = 200,
        null=True, 
        help_text=_("The company Country in which the company operates.")
    )

    company_share = models.CharField(
        verbose_name=_("Company Share"), 
        null=True, 
        max_length = 200,
        help_text=_("the number of shares the company is issuring")
        )
    
    business_logo = models.ImageField(
        verbose_name=_("Business Logo"),
        upload_to="business_document",
        null=True, 
        help_text=_("A business logo is a graphic or symbol that represents a company or brand. It is a visual representation of the business and plays a crucial role in establishing brand identity and recognition")
    )

    owner_name = models.CharField(
        verbose_name=_("Owner Name"),
        max_length = 200,
        null=True, 
        blank=True,
        help_text=_("this represents the name of the owner.")
    )

    non_compete_period = models.CharField(
        verbose_name=_("Non Compete Period"),
        max_length = 200,
        null=True, 
        help_text=_("the non completed period of the share agreements")
    )

    share_holders = models.ManyToManyField(
        Shares_Signatures,
        verbose_name=_("Share holder"),
        help_text=_('this represents the share holders details which includes the signatures ')
    )

    signature = models.ImageField(
        verbose_name=_("Signature"),
        upload_to="signatures",
        blank=True,
        null=True, 
        help_text=_("A business logo is a graphic or symbol that represents a company or brand. It is a visual representation of the business and plays a crucial role in establishing brand identity and recognition")
    )

    formatted_date = models.CharField(
        verbose_name=_("Formatted Date"), 
        null=True,
        blank=True,
        max_length=100,
        help_text=_("The date is formatted to when the agreement is taken.")
        )

    def __str__(self):
        return str(self.company_name)
    
    class Meta:
        ordering = ('-created_date',)
        verbose_name = _('Shares Agreements')
        verbose_name_plural = _('Shares Agreements') 



class Goods_And_Services_Agreement(BaseModel):
    """
    this holds the details and information about the goods 
    and services agreements
    """
    user = models.ForeignKey(
        User,
        verbose_name=_("User Account"),
        on_delete=models.CASCADE, null=True,
        related_name="agreement_owner_GnS",
        blank=True,
        help_text=_("The user associated with this business agreement.")
    )


    seller_name = models.CharField(
        verbose_name=_("Seller Name"),
        max_length = 200,
        null=True, 
        help_text=_("this represents the seller name .")
    )

    seller_address = models.CharField(
        verbose_name=_("Seller Address "),
        max_length = 200,
        null=True, 
        help_text=_("the seller home or work address.")
    )

    business_logo = models.ImageField(
        verbose_name=_("Business Logo"),
        upload_to="business_document",
        null=True, 
        help_text=_("A business logo is a graphic or symbol that represents a company or brand. It is a visual representation of the business and plays a crucial role in establishing brand identity and recognition")
    )

    owner_name = models.CharField(
        verbose_name=_("Owner Name"),
        max_length = 200,
        null=True, 
        help_text=_("this represents the owners name .")
    )

    seller_country = models.CharField(
        verbose_name=_("Seller Country"),
        max_length = 200,
        null=True, 
        help_text=_("The seller Country in which the seller operates.")
    )
    
    buyer_country = models.CharField(
        verbose_name=_("Buyer Country"),
        max_length = 200,
        null=True, 
        help_text=_("The Buyer Country in which the business operates.")
    )
    
    buyer_name = models.CharField(
        verbose_name=_("Buyer Name"),
        max_length = 200,
        null=True, 
        help_text=_("this represents the name of the buyer that is issuring the shares.")
    )

    buyer_address = models.CharField(
        verbose_name=_("Buyer Address"),
        max_length = 200,
        null=True, 
        help_text=_("this represents the buyer address.")
    )

    type = models.CharField(
        verbose_name=_("Type"),
        max_length = 200,
        null=True, 
        help_text=_("the type of the share agreement")
    )

    product_name = models.CharField(
        verbose_name=_("Product Name"),
        max_length = 200,
        null=True, 
        help_text=_("this represents the name of the product ")
    )

    product_quantity = models.CharField(
        verbose_name=_("Product Quantity"),
        max_length = 200,
        null=True, 
        help_text=_("this represents the quantity of the product ")
    )
        
    price_of_good_and_service = models.CharField(
        verbose_name=_("Price of Goods And Services"),
        blank=True,
        max_length = 200,
        null=True,  
        help_text=_("The price of good and service.")
        )
    
    delivery_address = models.CharField(
        verbose_name=_("Delivery Address"),
        max_length = 200,
        null=True, 
        help_text=_("the delivery service address.")
    )

    buyer_type = models.CharField(
        verbose_name=_("Buyer Type"),
        max_length = 200,
        null=True, 
        help_text=_("this holds the buyer type")
    )

    seller_type = models.CharField(
        verbose_name=_("Seller Type"),
        max_length = 200,
        null=True, 
        help_text=_("this holds the seller type")
    )

    signature = models.ImageField(
        verbose_name=_(" Signature"),
        upload_to="signatures",
        null=True, 
        blank=True,
        help_text=_("A business logo is a graphic or symbol that represents a company or brand. It is a visual representation of the business and plays a crucial role in establishing brand identity and recognition")
    )

    formatted_date = models.CharField(
        verbose_name=_("Formatted Date"), 
        null=True, 
        max_length = 200,
        blank=True,
        help_text=_("The date is formatted to when the agreement is taken.")
        )
    

    def __str__(self):
        return str(self.seller_name)
    
    class Meta:
        ordering = ('-created_date',)
        verbose_name = _('Goods and Services Agreements')
        verbose_name_plural = _('Goods and Services Agreements')




class Loan_Agreement (BaseModel):
    """
    this hold and represents the loan agreement information
    """

    user = models.ForeignKey(
        User,
        verbose_name=_("User Account"),
        on_delete=models.CASCADE, null=True,
        related_name="agreement_owner_LA",
        blank=True,
        help_text=_("The user associated with this business agreement.")
    )

    borrower_name = models.CharField(
        verbose_name=_("Borrower Name"),
        max_length = 200,
        null=True, 
        help_text=_("this is the full name of the borrower")
    )

    lender_name = models.CharField(
        verbose_name=_("Lender Name"),
        max_length = 200,
        null=True, 
        help_text=_("this is the full name of the lender")
    )

    amount = models.CharField(
        verbose_name=_("amount"),
        blank=True,
        max_length = 200,
        null=True,  
        help_text=_("The amount that will be issued.")
        )

    date_of_execution = models.CharField(
        verbose_name=_("Date Of Execution"), 
        max_length = 200,
        null=True, 
        blank=True,  
        help_text=_("The date of the execution.")
        )
    
    payment_frequency = models.CharField(
        verbose_name=_("Payment Frequency"),
        max_length = 200,
        null=True, 
        help_text=_("this holds the payment frequency.")
    )

    first_payment_date = models.CharField(
        verbose_name=_("First Payment Date"), 
        null=True,  
        blank=True,
        max_length=100,
        help_text=_("the first initial payment date is recorded.")
        )

    amount_of_each_payment = models.CharField(
        verbose_name=_("Amount Of Each Payment"),
        blank=True,
        max_length = 200,
        null=True,  
        help_text=_("The price of good and service.")
        )
    
    interest_name = models.CharField(
        verbose_name=_("Interest Name"), 
        null=True, 
        blank=True,
        max_length = 200,
        help_text=_("this have the percentage of the interest to be paid")
        )
    
    asset = models.CharField(
        verbose_name=_("Asset"),
        max_length = 200,
        null=True, 
        help_text=_("the record hold the asset, that is submitted for the loan")
    )

    lender_address = models.CharField(
        verbose_name=_("Lender Address"),
        max_length = 200,
        null=True, 
        help_text=_("the lender home or work address")
    )

    borrower_address = models.CharField(
        verbose_name=_("Borrower Address"),
        max_length = 200,
        null=True, 
        help_text=_("the borrower home or work address")
    )

    loaner_type = models.CharField(
        verbose_name=_("Loaner Type"),
        max_length = 200,
        null=True, 
        help_text=_("this holds the seller type")
    )

    asset_location = models.CharField(
        verbose_name=_("Asset Location"),
        max_length = 200,
        null=True, 
        help_text=_("the asset address")
    )

    borrower_type = models.CharField(
        verbose_name=_("Borrower Type"),
        max_length = 200,
        null=True, 
        help_text=_("this holds the borrower type")
    )

    lender_country = models.CharField(
        verbose_name=_("Lender Country"),
        max_length = 200,
        null=True, 
        help_text=_("The lender Country in which the business operates.")
    )
    
    business_logo = models.ImageField(
        verbose_name=_("Business Logo"),
        upload_to="business_document",
        null=True, 
        help_text=_("A business logo is a graphic or symbol that represents a company or brand. It is a visual representation of the business and plays a crucial role in establishing brand identity and recognition")
    )

    signature = models.ImageField(
        verbose_name=_(" Signature"),
        upload_to="signatures",
        null=True, 
        blank=True,
        help_text=_("A business logo is a graphic or symbol that represents a company or brand. It is a visual representation of the business and plays a crucial role in establishing brand identity and recognition")
    )

    formatted_date = models.CharField(
        verbose_name=_("Formatted Date"), 
        max_length = 200,
        null=True, 
        blank=True,  
        help_text=_("The date is formatted to when the agreement is taken.")
        )
    

    def __str__(self):
        return str(self.borrower_name)
    
    class Meta:
        ordering = ('-created_date',)
        verbose_name = _('Loan Agreements')
        verbose_name_plural = _('Loan Agreements')





    
    
    








