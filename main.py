from locust import HttpUser, SequentialTaskSet, task, constant

from faker import Faker

from pprint import pprint

import random

from datetime import date

from datetime import datetime, timedelta




fake = Faker()




class EmployeeOnboarding(SequentialTaskSet):




    employee_data = {}

    employee_id = None




    def on_start(self):

        self.client.headers = {

            'Authorization': 'token 23de9aa2ae5d3ae:9f72416c7fdc012'

        }

        self.company = 'SUGAR'




    #need to submit

    #Done

    @task(1)

    def shift_assignment(self):

        if not self.employee_id:

            employee_info = self.create_employee()

            self.employee_id = employee_info["employee_id"]




        shift_type = {

            "employee": self.employee_id,

            "shift_type": "Regular Shift",

            "start_date": str(fake.date_this_month()),

        }




        with self.client.post("/api/resource/Shift Assignment", json=shift_type) as response:

            assert response.status_code == 200, f"Shift Assignment failed. response: {response.text}"




            created_shift_assignment = response.json().get("data").get("name")




            shift = {"name": created_shift_assignment, "docstatus": 1}

            with self.client.put(f"/api/resource/Shift Assignment/{created_shift_assignment}", json=shift) as resp_update:

                assert resp_update.status_code == 200, f"Shift Assignment failed. Response: {resp_update.text}"

                print(f"Shift Assignment Submitted Successfully for Employee ID: {self.employee_id}")




    #need to submit

    #Done

    @task(1) 

    def create_salary_structure(self):

        if not self.employee_id:

            employee_info = self.create_employee()

            self.employee_id = employee_info["employee_id"]




        salary_structure = self.get_salary_structure()

        if not salary_structure:

            print("Error: No valid salary structures available for assignment.")

            return




        salary_struct = {

            "employee": self.employee_id,

            "salary_structure": random.choice(salary_structure),

            "from_date": str(date.today()),

            "base_per_annum": fake.random_number(digits=6),

            "base": fake.random_number(digits=6),

            "ctc": fake.random_number(digits=6),

        }




        with self.client.post("/api/resource/Salary Structure Assignment", json=salary_struct, catch_response=True) as resp:

            assert resp.json() is not None

            print("Salary Structure Assignment Created Successfully")




            created_salary_assignment = resp.json().get("data").get("name")




            salary = {"name": created_salary_assignment, "docstatus": 1}

            with self.client.put(f"/api/resource/Salary Structure Assignment/{created_salary_assignment}", json=salary) as resp_update:

                assert resp_update.status_code == 200, f"Salary Structure Assignment failed. Response: {resp_update.text}"

                print(f"Salary Structure Assignment Submitted Successfully for Employee ID: {self.employee_id}")




    #need to submit

    #Done

    @task(1) 

    def employee_tax_exemption(self):

        if not self.employee_id:

            employee_info = self.create_employee()

            self.employee_id = employee_info["employee_id"]




        payroll_period = self.get_payroll_period()

        income_tax_slab = self.get_income_tax_slab()

        component= self.get_salary_component()




        tax = {

            "employee": self.employee_id,

            "payroll_period": random.choice(payroll_period),

            "currency": 'INR',

            "income_tax_slab": random.choice(income_tax_slab),

            "benefit_preference": [

                {"component": "Mobile & Internet", "preference": "Claim based on Expense"},

                {"component": "Books & Periodicals", "preference": "Claim based on Expense"},

                {"component": "Leave Travel Allowance", "preference": "Claim based on Expense"},

            ]

        }




        with self.client.post("/api/resource/Employee Tax Exemption Declaration", json=tax) as resp:

            assert resp.json() is not None




            created_employee_tax = resp.json().get("data").get("name")




            shift = {"name": created_employee_tax, "docstatus": 1}

            with self.client.put(f"/api/resource/Employee Tax Exemption Declaration/{created_employee_tax}", json=shift) as resp_update:

                assert resp_update.status_code == 200, f"Employee Tax Exemption Declaration failed. Response: {resp_update.text}"

                print(f"Employee Tax Exemption Declaration Submitted Successfully for Employee ID: {self.employee_id}")







    #Done

    @task(1)

    def leave_assignment(self):

        if not self.employee_id:

            employee_info = self.create_employee()

            self.employee_id = employee_info["employee_id"]




        leave_assignment_type = {

            "employee": self.employee_id,

            "leave_policy": "HR-LPOL-2024-00001",

            "assignment_base_on": "Joining Date",

            "effective_to": fake.future_date().strftime("%Y-%m-%d"),

            "effective_from": fake.date_this_month().strftime("%Y-%m-%d"),

        }




        with self.client.post("/api/resource/Leave Policy Assignment", json=leave_assignment_type, catch_response=True) as resp:

            assert resp.json() is not None




            leave_assignment = resp.json().get("data").get("name")




            holid = {"name": leave_assignment, "docstatus": 1}

            with self.client.put(f"/api/resource/Leave Policy Assignment/{leave_assignment}", json=holid) as resp_update:

                assert resp_update.status_code == 200, f"leave Policy Assignment failed. Response: {resp_update.text}"

                print(f"leave Policy Assignment Submitted Successfully for Employee ID: {self.employee_id}")







    #Done

    @task(1)

    def create_employee_checkin(self):

        if not self.employee_id:

            employee_info = self.create_employee()

            self.employee_id = employee_info["employee_id"]




        check_in = {

            "employee": self.employee_id,

            "time": str(fake.date_time_this_month()),

            "log_type": 'IN',

        }




        with self.client.post("/api/resource/Employee Checkin", json=check_in) as resp:

            assert resp.json() is not None

            print(f"Employee Checkin Created Successfully for Employee ID: {self.employee_id}")




    #Done

    @task(1)

    def create_holiday_assignment(self):

        holiday_list = self.get_holiday_list()

        if not self.employee_id:

            employee_info = self.create_employee()

            self.employee_id = employee_info["employee_id"]




        holiday = {

            "employee": self.employee_id,

            # "holiday_list": random.choice(holiday_list),

            "holiday_list": "Weekly Off",

            "posting_date": str(fake.date_this_month()),

            "applicable_from": str(fake.date_this_month())

        }




        with self.client.post("/api/resource/Holiday Assignments", json=holiday) as resp:

            assert resp.json() is not None




            holiday_assignment = resp.json().get("data").get("name")




            holid = {"name": holiday_assignment, "docstatus": 1}

            with self.client.put(f"/api/resource/Holiday Assignments/{holiday_assignment}", json=holid) as resp_update:

                assert resp_update.status_code == 200, f"Holiday Assignments failed. Response: {resp_update.text}"

                print(f"Holiday Assignments Submitted Successfully for Employee ID: {self.employee_id}")




    #Done

    @task(1)

    def create_leave_application(self):

        leave_list = self.get_holiday_list()

        user_list = self.get_users()




        if not self.employee_id:

            employee_info = self.create_employee()

            self.employee_id = employee_info["employee_id"]




        start_date = fake.date_this_month()

        end_date = start_date + timedelta(days=2)




        leave_application = {

            "employee": self.employee_id,

            'leave_type': "Leave Without Pay",

            # "leave_type": random.choice(leave_list),

            "from_date": start_date.strftime("%Y-%m-%d"),

            "to_date": end_date.strftime("%Y-%m-%d"),

            "workflow_table": [

                {

                    "user": random.choice(user_list),

                }

            ]

        }




        with self.client.post("/api/resource/Leave Application", json=leave_application, catch_response=True) as resp:

            if resp.status_code != 200:

                if "ValidationError" in resp.text and "Application period cannot be outside leave allocation period" in resp.text:

                    resp.failure(f"Invalid leave application dates: {leave_application['from_date']} to {leave_application['to_date']}")

                else:

                    resp.failure(f"Request failed with status code {resp.status_code}. Response text: {resp.text}")

            else:

                assert resp.json() is not None

                print(f"Leave Application Successful for Employee ID: {self.employee_id}")




    #Done

    @task(1) 

    def leave_allowance_allocation(self):

        if not self.employee_id:

            employee_info = self.create_employee()

            self.employee_id = employee_info["employee_id"]




        lta_policy = self.get_leave_policy()

        policy= {

            "employee": self.employee_id,

            "lta_policy": random.choice(lta_policy),

            "posting_date": str(date.today()),

            "applicable_from": str(fake.date_this_month())




        }




        with self.client.post("/api/resource/Leave Travel Allowance Allocation", json=policy) as resp:

            assert resp.json() is not None




            submit_leave_allocation = resp.json().get("data").get("name")




            leave = {"name": submit_leave_allocation, "docstatus": 1}

            with self.client.put(f"/api/resource/Leave Travel Allowance Allocation/{submit_leave_allocation}", json=leave) as resp_update:

                assert resp_update.status_code == 200, f"Leave Travel Allowance Allocation failed. Response: {resp_update.text}"

                print(f"Leave Travel Allowance Allocation Submitted Successfully for Employee ID: {self.employee_id}")




    #Done

    @task(1) 

    def attendance(self):

        status = ["Present","Absent","On Leave","Half Day","Work From Home","Holiday"]

        if not self.employee_id:

            employee_info = self.create_employee()

            self.employee_id = employee_info["employee_id"]




        attendance = {

            "employee": self.employee_id,

            "status": "Present",

            "attendance_date": str(date.today()),			

            # "status": random.choice(status),

        }




        with self.client.post("/api/resource/Attendance", json=attendance) as response:

            assert response.json() is not None




            submit_attendance = response.json().get("data").get("name")




            attend = {"name": submit_attendance, "docstatus": 1}

            with self.client.put(f"/api/resource/Attendance/{submit_attendance}", json=attend) as resp_update:

                assert resp_update.status_code == 200, f"Shift Assignment failed. Response: {resp_update.text}"

                print(f"Attendance Submitted Successfully for Employee ID: {self.employee_id}")




    #Done          

    @task(1) 

    def create_expense_claim(self):




        employee_name = ''




        if not self.employee_id:

            employee_info = self.create_employee()

            self.employee_id = employee_info["employee_id"]

            employee_name = employee_info["employee_name"]




        expense_claim_type = self.get_expense_claim_type()

        account = self.get_account()

        user = self.get_users()

        expenses = [

            {

                "expense_type": random.choice(expense_claim_type),

                "amount": fake.random_number(digits=4),

                "default_account": random.choice(account),

                "expense_date": str(date.today())

            }

        ]

        expense_claim = {

            "employee": self.employee_id,

            "payable_account": random.choice(account),

            "expenses": expenses,

            "expense_approver": random.choice(user),

            "title": employee_name

        }




        with self.client.post("/api/resource/Expense Claim", json=expense_claim) as resp:

            assert resp.json() is not None

            print(f"Expense Claim Created Successfully for Employee ID: {self.employee_id}")




            expense_cl = resp.json().get("data").get("name")




            expense = {"name": expense_cl, "docstatus": 1}

            with self.client.put(f"/api/resource/Expense Claim/{expense_cl}", json=expense) as resp_update:

                assert resp_update.status_code == 200, f"Expense Claim failed. Response: {resp_update.text}"

                print(f"Expense Claim Submitted Successfully for Employee ID: {self.employee_id}")




    @task(1)

    def employee_benefit_application(self):

        if not self.employee_id:

            employee_info = self.create_employee()

            self.employee_id = employee_info["employee_id"]




        payroll_period = self.get_payroll_period()




        benefit = {

                "employee": self.employee_id,

                "date": str(date.today()),

                "payroll_period": random.choice(payroll_period),

                "employee_benefits": [

                    {"earning_component": "Mobile & Internet", "amount": "0.00"},

                    {"earning_component": "Books & Periodicals", "amount": "0.00"},

                    {"earning_component": "Leave Travel Allowance", "amount": "0.00"},

                ]

            }




        try:

            with self.client.post("/api/resource/Employee Benefit Application", json=benefit, catch_response=True) as resp:

                assert resp.json() is not None

                pprint(resp.json())

                print(f"Employee Benefit Application Successfully Created for Employee ID: {self.employee_id}")

        except Exception as e:

            print(f"An error occurred: {e}")




    #Done

    @task(1) 

    def payroll_entry(self):




        if not self.employee_id:

            employee_info = self.create_employee()

            self.employee_id = employee_info["employee_id"]




        cost_center = self.get_cost_center()

        user_list = self.get_users()




        payroll= {

            "employee_filter": self.employee_id,

            "posting_date": str(date.today()),

            "payroll_frequency": "Monthly",

            "currency": "INR",

            "exchange_rate": "1",

            "payroll_payable_account": "Payroll Payable - S",

            "start_date": str(fake.date_this_month()),

            "end_date": str(fake.future_date()),

            "cost_center": random.choice(cost_center),

            "employees":[

                {

                    "employee": self.employee_id

                }

            ],

            "workflow_table": [

                {

                    "user": random.choice(user_list),

                }

            ]

        }




        with self.client.post("/api/resource/Payroll Entry", json=payroll) as resp:

            assert resp.json() is not None

            print(f"Payroll Entry Created Successfully for Employee ID: {self.employee_id}")




            payroll_ent = resp.json().get("data").get("name")




            pay_en = {"name": payroll_ent, "docstatus": 1}

            with self.client.put(f"/api/resource/Payroll Entry/{payroll_ent}", json=pay_en) as resp_update:

                assert resp_update.status_code == 200, f"Payroll Entry failed. Response: {resp_update.text}"

                print(f"Payroll Entry Submitted Successfully for Employee ID: {self.employee_id}")




    #Done

    @task(1) 

    def salaryslip(self):




        with self.client.post("/api/method/stanch.after_migrate.submit_salary_slips") as response:

            assert response.json() is not None

            print(f"Salary Slip Submitted Successfully for Employee ID: {self.employee_id}")

            print("All Done")







    def create_employee(self):

        user_list = self.get_users()

        department_names = self.get_department()

        designation_names = self.get_designation()

        branch_names = self.get_branch()

        work_location = self.get_work_location_state()

        self.gender = ["Male", "Female"]




        first_name = fake.first_name()

        last_name = fake.last_name()

        full_name = first_name + " " + last_name

        employee_email = f"{full_name.lower().replace(' ', '_')}@stanch.io"




        existing_employee_id = self.get_employee_by_email(employee_email)

        if existing_employee_id:

            self.employee_id = existing_employee_id

            print(f"Employee with email {employee_email} already exists. Using existing employee ID: {existing_employee_id}")

            return existing_employee_id




        employee_data = {

            "first_name": first_name,

            "last_name": last_name,

            "company_email": employee_email,

            "department": random.choice(department_names),

            "designation": random.choice(designation_names),

            "branch": random.choice(branch_names),

            "gender": random.choice(self.gender),

            "date_of_birth": str(fake.date_of_birth()),

            "date_of_joining": str(date.today()),

            "aadhaar_no": fake.msisdn(),

            "pan_number": fake.pystr(),

            "work_location_state": random.choice(work_location),

            "leave_approver": random.choice(user_list),

            "expense_approver": random.choice(user_list),

        }




        with self.client.post("/api/resource/Employee", json=employee_data, catch_response=True) as resp:

            if resp.status_code != 200:

                resp.failure(f"Request failed with status code {resp.status_code}. Response text: {resp.text}")

            else:

                assert resp.json() is not None

                print("Employee Created Succesfully")




        self.employee_id = resp.json().get('data', {}).get('name')




        return {"employee_id": self.employee_id, "employee_name": full_name}




    def get_employee_by_email(self, email):

        query_params = {

            "filters": {"company_email": email},

            "fields": ["name"],

        }




        with self.client.get("/api/resource/Employee", params=query_params, catch_response=True) as resp:

            if resp.status_code != 200:

                resp.failure(f"Request failed with status code {resp.status_code}. Response text: {resp.text}")

                return None




            employee_data = resp.json().get("data", [])

            if employee_data:

                return employee_data[0].get("name")

            return None







    @task(1)

    def get_salary_component(self):

        with self.client.get("/api/resource/Salary Component") as resp:

            assert resp.json() is not None

            salary = resp.json().get("data", [])

            salary_component= [sal.get("name") for sal in salary]

            return salary_component




    @task(1)

    def get_expense_claim_type(self):

        with self.client.get("/api/resource/Expense Claim Type") as resp:

            assert resp.json() is not None

            expense_claim = resp.json().get("data", [])

            expense_claim_type= [expense.get("name") for expense in expense_claim]

            return expense_claim_type




    @task(1)

    def get_salary_structure(self):

        with self.client.get("/api/resource/Salary Structure") as resp:

            assert resp.json() is not None

            salary_struct = resp.json().get("data", [])

            salary_structure = [struct.get("name") for struct in salary_struct]

            return salary_structure




    @task(1)

    def get_account(self):

        with self.client.get("/api/resource/Account") as resp:

            assert resp.json() is not None

            account = resp.json().get("data", [])

            account_type= [acc.get("name") for acc in account]

            return account_type




    @task(1)

    def get_leave_policy(self):

        with self.client.get("/api/resource/Leave Travel Allowance Policy") as resp:

            assert resp.json() is not None

            policy = resp.json().get("data", [])

            leave_policy = [poli.get("name") for poli in policy]

            return leave_policy




    @task(1)

    def get_payroll_period(self):

        with self.client.get("/api/resource/Payroll Period") as resp:

            assert resp.json() is not None

            payroll = resp.json().get("data", [])

            payroll_period = [pay.get("name") for pay in payroll]

            return payroll_period







    @task(1)

    def get_income_tax_slab(self):

        with self.client.get("/api/resource/Income Tax Slab") as resp:

            assert resp.json() is not None

            income_tax = resp.json().get("data", [])

            income_tax_slab = [tax.get("name") for tax in income_tax]

            return income_tax_slab




    @task(1)

    def get_department(self):

        with self.client.get("/api/resource/Department") as resp:

            assert resp.json() is not None

            department_data = resp.json().get("data", [])

            department_names = [department.get("name") for department in department_data]

            return department_names




    @task(1)

    def get_designation(self):

        with self.client.get("/api/resource/Designation") as resp:

            assert resp.json() is not None

            designation_data = resp.json().get("data", [])

            designation_names = [designation.get("name") for designation in designation_data]

            return designation_names




    @task(1)

    def get_branch(self):

        with self.client.get("/api/resource/Branch") as resp:

            assert resp.json() is not None

            branch_data = resp.json().get("data", [])

            branch_names = [branch.get("name") for branch in branch_data]

            return branch_names




    @task(1)

    def get_work_location_state(self):

        with self.client.get("/api/resource/Work Location State") as resp:

            assert resp.json() is not None

            location = resp.json().get("data", [])

            work_location = [loc.get("name") for loc in location]

            return work_location




    @task(1)

    def get_holiday_list(self):

        with self.client.get("/api/resource/Holiday List") as resp:

            assert resp.json() is not None

            holiday_data = resp.json().get("data", [])

            holiday = [holi.get("name") for holi in holiday_data]

            return holiday




    @task(1)

    def get_users(self):

        with self.client.get("/api/resource/User") as resp:

            assert resp.json() is not None

            user_data = resp.json().get("data", [])

            users = [user.get("name") for user in user_data]

            return users




    @task(1)

    def get_cost_center(self):

        with self.client.get("/api/resource/Cost Center") as resp:

            assert resp.json() is not None

            datas = resp.json().get("data", [])

            data = [d.get("name") for d in datas]

            # pprint(data)

            return data




    @task

    def get_employee(self):

        with self.client.get("/api/resource/Employee") as resp:

            assert resp.json() is not None

            # pprint(resp.json())




    @task

    def get_leave_policy_assignment(self):

        with self.client.get("/api/resource/Leave Policy Assignment") as resp:

            assert resp.json() is not None

            # pprint(resp.json())




    @task

    def get_shift_assignment(self):

        with self.client.get("/api/resource/Shift Assignment") as resp:

            assert resp.json() is not None

            # pprint(resp.json())




    @task

    def get_holiday_assignments(self):

        with self.client.get("/api/resource/Holiday Assignments") as resp:

            assert resp.json() is not None

            # pprint(resp.json())




    @task

    def get_employee_checkin(self):

        with self.client.get("/api/resource/Employee Checkin") as resp:

            assert resp.json() is not None

            # pprint(resp.json())




    @task

    def get_attendance(self):

        with self.client.get("/api/resource/Attendance") as resp:

            assert resp.json() is not None

            # pprint(resp.json())




    @task

    def get_expense_claim(self):

        with self.client.get("/api/resource/Expense Claim") as resp:

            assert resp.json() is not None

            # pprint(resp.json())




    @task

    def get_leave_application(self):

        with self.client.get("/api/resource/Leave Application") as resp:

            assert resp.json() is not None

            # pprint(resp.json())




    @task

    def get_salary_structure_assignment(self):

        with self.client.get("/api/resource/Salary Structure Assignment") as resp:

            assert resp.json() is not None

            # pprint(resp.json())







    @task

    def get_employee_benefit_application(self):

        with self.client.get("/api/resource/Employee Benefit Application") as resp:

            assert resp.json() is not None

            # pprint(resp.json())




    @task

    def get_tax_exemption_declaration(self):

        with self.client.get("/api/resource/Employee Tax Exemption Declaration") as resp:

            assert resp.json() is not None

            # pprint(resp.json())




    @task

    def get_leave_travel_allowance(self):

        with self.client.get("/api/resource/Leave Travel Allowance Allocation") as resp:

            assert resp.json() is not None

            # pprint(resp.json())




    @task

    def get_payroll_entry(self):

        with self.client.get("/api/resource/Payroll Entry") as resp:

            assert resp.json() is not None

            # pprint(resp.json())







    @task

    def get_customer(self):

        with self.client.get("/api/resource/Customer") as resp:

            assert resp.json() is not None

            # pprint(resp.json())







    @task

    def get_supplier(self):

        with self.client.get("/api/resource/Supplier") as resp:

            assert resp.json() is not None

            # pprint(resp.json())




    @task

    def get_item(self):

        with self.client.get("/api/resource/Item") as resp:

            assert resp.json() is not None

            # pprint(resp.json())




    @task(1)

    def get_trial_balance(self):

        name = self.create_employee()

        company = name.get("data", {}).get('company')

        with self.client.get(f"/api/method/frappe.desk.query_report.run?report_name=Trial Balance&filters={{\"company\":\"{company}\",\"fiscal_year\":\"2023-2024\",\"from_date\":\"2023-04-01\",\"to_date\":\"2024-03-31\",\"with_period_closing_entry\":1,\"show_unclosed_fy_pl_balances\":1,\"include_default_book_entries\":1}}") as resp:

            assert resp.json() is not None

            # pprint(resp.json())	




    @task

    def get_general_ledger(self):

        name = self.create_employee()

        company = name.get("data", {}).get('company')

        with self.client.get(f"/api/method/frappe.desk.query_report.run?report_name=General Ledger&filters={{\"company\":\"{company}\",\"from_date\":\"2023-12-22\",\"to_date\":\"2023-12-22\",\"voucher_no\":\"PINV-23-00109\",\"group_by\":\"Group by Voucher (Consolidated)\",\"include_dimensions\":1}}") as resp:

            assert resp.json() is not None

            # pprint(resp.json())	




    @task

    def get_balance_sheet(self):

        name = self.create_employee()

        company = name.get("data", {}).get('company')

        with self.client.get(f"/api/method/frappe.desk.query_report.run?report_name=Balance Sheet&filters={{\"company\":\"{company}\",\"filter_based_on\":\"Fiscal Year\",\"period_start_date\":\"2023-04-01\",\"period_end_date\":\"2024-03-31\",\"from_fiscal_year\":\"2023-2024\",\"to_fiscal_year\":\"2023-2024\",\"periodicity\":\"Yearly\",\"accumulated_values\":1,\"include_default_book_entries\":1}}") as resp:

            assert resp.json() is not None

            # pprint(resp.json())




    @task(1)

    def stop(self):

        self.interrupt(reschedule=True)




class TestUser(HttpUser):

    host = 'https://suga.staging.stanch.io'

    wait_time = constant(30)




    tasks = [EmployeeOnboarding]




    def on_request_success(self, request_type, name, response_time, response_length, **kwargs):

        if request_type == "create_employee":

            self.tasks[0].create_mapping_document()




if __name__ == "__main__":

    TestUser().run()
