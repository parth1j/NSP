import mysql.connector

columns = {
   'students': ['student_id', 'student_details'], 
   'addresses': ['address_id', 'line_1', 'line_2', 'city', 'zip_postcode', 'state_province_county', 'country'], 
   'people': ['person_id', 'first_name', 'middle_name', 'last_name', 'cell_mobile_number', 'email_address', 'login_name', 'password'], 
   'courses': ['course_id', 'course_name', 'course_description', 'other_details'], 
   'people_addresses': ['person_address_id', 'person_id', 'address_id', 'date_from', 'date_to'], 
   'student_course_registrations': ['student_id', 'course_id', 'registration_date'], 
   'candidates': ['candidate_id', 'candidate_details'], 
   'candidate_assessments': ['candidate_id', 'qualification', 'assessment_date', 'asessment_outcome_code'],
   'department': ['Department_ID', 'Name', 'Creation', 'Ranking', 'Budget_in_Billions', 'Num_Employees'],
   'head': ['head_ID', 'name', 'born_state', 'age'], 
   'management': ['department_ID', 'head_ID', 'temporary_acting'], 
   'city': ['City_ID', 'Official_Name', 'Status', 'Area_km_2', 'Population', 'Census_Ranking'], 
   'farm': ['Farm_ID', 'Year', 'Total_Horses', 'Working_Horses', 'Total_Cattle', 'Oxen', 'Bulls', 'Cows', 'Pigs', 'Sheep_and_Goats'], 
   'farm_competition': ['Competition_ID', 'Year', 'Theme', 'Host_city_ID', 'Hosts'],
   'competition_record': ['Competition_ID', 'Farm_ID', 'ranks']
}

class Database:
    def __init__(self):
       self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            database="spider",
            passwd="fekboig",
            auth_plugin='mysql_native_password'
        )

    
    def execute(self,query)->list:
        cur = self.mydb.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        field_names = [i[0] for i in cur.description]
        return (field_names,rows)
    
    def get_columns(self,table)->list:
        return columns[table] if table in columns else []
    
    def get_tables(self)->list:
        cur = self.mydb.cursor()
        cur.execute("SELECT table_name FROM information_schema.tables;")
        return [x[0] for x in cur.fetchall()]
