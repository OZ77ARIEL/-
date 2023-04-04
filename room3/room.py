# Create a sample DataFrame
import pandas as pd
import numpy as np
import random
import re
import json
# print error if the number of students matches the total number of beds in all rooms
def to_mach_students():
    html_template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Page Title</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                font-family: Arial, sans-serif;
            }}
            
            h1 {{
                margin-top: 0;
                text-align: center;
                font-size: 72px;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <h1>{text}</h1>
    </body>
    </html>
    '''

    rooms = html_template.format(text='יש יותר תלמידים ממקום בחדרים')

    with open('טבלת שיבוץ חדרים ראשונית.html', 'w') as f:
        f.write(rooms)

    exit()

    # Initialize the table HTML code
    html_code="	<title>שיבוץ חדרים סופי</title><style>.center {position: absolute;top: 70%;left: 50%;transform: translate(-50%, -50%);text-align: center;font-size: 48px;font-weight: bold;}</style>"
    
    html_code += '<table id="room-table" border="4" style="width: 70%; height: 60%; margin:auto; table-layout:fixed;">'

    # Add the table headers row
    html_code += '<tr>'
    for col in rooms.columns:
        html_code += '<th>{}</th>'.format(col)
    html_code += '</tr>'
    
    # Add the table data rows
    for i in range(len(rooms)):
        html_code += '<tr>'
        for j in range(len(rooms.columns)):
            if rooms.iloc[i, j] == 0:
                html_code += '<td style="background-color: black;"></td>'
            elif rooms.iloc[i, j][1] == 0:
                html_code += '<td style="text-align:center; border-right: 3px solid black;border-left: 3px solid black; font-weight:bold;" onclick="swapCell(this);" onmousedown="selectCell(this);" onmouseup="deselectCell(this);">{}</td>'.format(rooms.iloc[i, j][0])
            elif rooms.iloc[i, j][1] == -1:
                html_code += '<td style="text-align:center; background-color: red ; border-right: 3px solid black;border-left: 3px solid black; font-weight:bold;" onclick="swapCell(this);" onmousedown="selectCell(this);" onmouseup="deselectCell(this);">{}</td>'.format(rooms.iloc[i, j][0])
            elif rooms.iloc[i, j][1] == 1:
                html_code += '<td style="text-align:center; background-color: green ; border-right: 3px solid black;border-left: 3px solid black; font-weight:bold;" onclick="swapCell(this);" onmousedown="selectCell(this);" onmouseup="deselectCell(this);">{}</td>'.format(rooms.iloc[i, j][0])

        html_code += '</tr>'

    # Close the table HTML code
    html_code += '</table>'
    html_code +="<body><h1 class=\"center\">שיבוץ חדרים</h1></body>"
    return html_code

def check_duplicate_strings(list1, list2):
    """
    Function to check if there are any duplicate strings that appear in both
    given lists of strings. Returns True if there are any such strings,
    otherwise False.
    """
    if (list1==[] or list2==[]):
      return False
    seen_strings = set()
    for string in list1:
        if string in seen_strings:
            return True
        seen_strings.add(string)
    for string in list2:
        if string in seen_strings:
            return True
        seen_strings.add(string)
    return False

def add_love_heate(students,love_heate):
    new_student_list=[]
    for name in students:
        if (name!='פנוי'):
            l=list(love_heate.iloc[:,0])
            row=l.index(name)
            student_card=[name,love_heate.iloc[row,1],love_heate.iloc[row,2],[4]]
            new_student_list.append(student_card)
        else:    
            student_card=[name,[],[],[4]]
            new_student_list.append(student_card)  
        
    for i in range(len(new_student_list)):
            if(check_duplicate_strings(new_student_list[i][2],students)):
                new_student_list[i][3]=-1
            elif(check_duplicate_strings(new_student_list[i][1],students)):
                new_student_list[i][3]=1
    return (new_student_list)

# read the Excel file into a pandas dataframe
all = pd.read_excel('room.xlsx')
df = all.iloc[:, [0, 3, 4]]
b= all.iloc[:, [0, 1, 2]]
love_heate=b
for i,name in enumerate((b.iloc[:,0])):
  love_heate.iloc[i,1] = re.split('[ ,.]+\s*',str(b.iloc[i,1]))
  love_heate.iloc[i,2] = re.split('[ ,.]+\s*',str(b.iloc[i,2]))


# check if the number of students matches the total number of beds in all rooms
if df.iloc[:, 2].sum() < df.iloc[:, 0].count():
   to_mach_students()
# add extra students named "פנוי" to make the total number of students equal to the total number of beds
while df.iloc[:, 2].sum() > df.iloc[:, 0].count():
    df.loc[len(df.index)] = ['פנוי' ,np.nan, np.nan]
df.iloc[:,0] = random.sample(df.iloc[:,0].tolist(), len(df.iloc[:,0]))

# create a new dataframe named "rooms" that contains the name of each room and a list of students in that room
data={}
i=0
max_place_in_room=max(df.iloc[:, 2])

for index,room_name in enumerate(df.iloc[:, 1].unique()):
    room = df.loc[df.iloc[:, 1] == room_name]
    if not room.empty:
        place_in_room = int(df.iloc[index, 2]) 
        students =list(df.iloc[i:i+place_in_room, 0])
        students_list=add_love_heate(students,love_heate)

        while len(students_list)<max_place_in_room:
            students_list=students_list + [0]
        data[room_name]= students_list
        i=i+place_in_room

# Define the JavaScript code for cell swapping and selection
start_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>שיבוצ חדרים</title>
        <style>
		h1 {text-align: center;}
        </style>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.3.2/html2canvas.min.js"></script>

    </head>
    <body>
        <div id="table-container" ></div>
        <script>
            var data =
            """
        
        
end_code="""
          var selectedRow = null;
        var selectedCol = null;
        var rooms = Object.keys(data);
        
        function takeScreenshot() {
            displayWhiteTable()
			html2canvas(document.getElementById("table-container")).then(function(canvas) {
				var imgData = canvas.toDataURL('image/png');
				var filename = 'שיבוץ חדרים.png';
				saveScreenshot(imgData, filename);
			});
            displayTable()
        }

		function saveScreenshot(data, filename) {
			var a = document.createElement('a');
			a.href = data;
			a.download = filename;
			document.body.appendChild(a);
			a.click();
			document.body.removeChild(a);
		}
        
        function handleClick(row, col) {
        	  if(data[rooms[col]][row]!==0){
                if (selectedRow === null && selectedCol === null) {
                    selectedRow = row;
                    selectedCol = col;
                    data[rooms[col]][row][3]=3;
                } else {
                    var temp = data[rooms[selectedCol]][selectedRow];
                    data[rooms[selectedCol]][selectedRow] = data[rooms[col]][row];
                    data[rooms[col]][row]= temp;	
                    changedata(col)
                    changedata(selectedCol);
                    selectedRow = null;
                    selectedCol = null;




              } 
              }
              displayTable();
       	   
		}
		
		
		function checkStringInList(str, list) {
			if (typeof str !== 'string') {
				return false;
			}
			if (!list) {
				return false;
			}
			return list.includes(str);
		}
		
		function changedata(col) {
				
			for (var i = 0; i < data[rooms[col]].length; i++){
				data[rooms[col]][i][3]=4;
			}
					
			for (var i = 0; i < data[rooms[col]].length; i++){
                if(data[rooms[col]][i]!=0){
					for (var h = 0; h < data[rooms[col]].length; h++){
                            if (data[rooms[col]][h]==0){}
							else if (data[rooms[col]][h][3]==-1){}
							else if (data[rooms[col]][h][3]==1){
								const want = data[rooms[col]][h][1];
								const dont_want = data[rooms[col]][h][2];
								const child = data[rooms[col]][i][0];
								if (checkStringInList(child,dont_want)){
									data[rooms[col]][h][3]=-1;
								}
							}
							else if (data[rooms[col]][h][3]==4){
								const want = data[rooms[col]][h][1];
								const dont_want = data[rooms[col]][h][2];
								const child = data[rooms[col]][i][0];
								
								 if (checkStringInList(child,dont_want)){
									data[rooms[col]][h][3]=-1;
									}
									
								else if(checkStringInList(child,want)){
										data[rooms[col]][h][3]=1;
								}	
								
							}
					}
				}
            }
		}
		
        function displayTable() {
			
            var table = '<table><table style="width: 70%; height: 20%; margin:auto; table-layout:fixed;"><tr>';
            for (var i = 0; i < rooms.length; i++) {
                table += '<th>' + rooms[i] + '</th>';
            }
            table += '</tr>';
            var maxRows = 0;
            for (var room in data) {
                if (data[room].length > maxRows) {
                    maxRows = data[room].length;
                }
            }
            for (var i = 0; i < maxRows; i++) {
                table += '<tr>';
                for (var j = 0; j < rooms.length; j++) {
                    if (i < data[rooms[j]].length) {
                        table += '<td  style="background-color:';
                        if (data[rooms[j]][i][3] == 4) {
                            table += ' white;';}
                        else if (data[rooms[j]][i][3] === -1) {
                            table += ' red;';}
                        else if (data[rooms[j]][i][3] === 1) {
                            table += ' lightgreen;';    
                        }
                        else if (data[rooms[j]][i] === 0) {
                            table += ' grey;';    
                        }
                        
                        else if (data[rooms[j]][i][3] === 3) {
                            table += ' lightblue;';    
                        }
                        table += ' height: 50px; word-wrap: break-word; border: 1px solid grey; text-align:center; border-right: 4px solid black;border-left: 4px solid black; font-weight:bold;"'
                        table += ' onclick="handleClick(' + i + ',' + j + ')">';
                        table += [data[rooms[j]][i][0]] || '';
                        table += '</td>';
                    } else {
                        table += '<td></td>';
                    }
                }
                table += '</tr>';
            }
            table += '</table>';
           
            document.getElementById('table-container').innerHTML = table;
        }
        
        
        function displayWhiteTable() {
			
            var table = '<table><table style="width: 70%; height: 20%; margin:auto; table-layout:fixed;"><tr>';
            for (var i = 0; i < rooms.length; i++) {
                table += '<th>' + rooms[i] + '</th>';
            }
            table += '</tr>';
            var maxRows = 0;
            for (var room in data) {
                if (data[room].length > maxRows) {
                    maxRows = data[room].length;
                }
            }
            for (var i = 0; i < maxRows; i++) {
                table += '<tr>';
                for (var j = 0; j < rooms.length; j++) {
                    if (i < data[rooms[j]].length) {
                        if (data[rooms[j]][i] == 0) {
                           table += '<td  style="background-color:grey;'}
                        else{
                           table += '<td  style="background-color:white;'}
                        table += ' height: 50px; word-wrap: break-word; border: 1px solid grey; text-align:center; border-right: 4px solid black;border-left: 4px solid black; font-weight:bold;"'
                        table += ' onclick="handleClick(' + i + ',' + j + ')">';
                        table += [data[rooms[j]][i][0]] || '';
                        table += '</td>';
                    } else {
                        table += '<td></td>';
                    }
                }
                table += '</tr>';
            }
            table += '</table>';
           
            document.getElementById('table-container').innerHTML = table;
        }
        
        displayTable();
  
    </script>
    <h1> שיבוץ חדרים </h1>
    <div style="text-align: center;">
         <button style="width: 100px; height: 50px; margin: 0 auto;" onclick="takeScreenshot()">שמירת טבלה</button>
    </div>
    <h1></h1>
    <h1></h1>
    <h13> ©עוז אריאל </h13>
    </body>
</html>

"""

# Combine the HTML and JavaScript code

# Save the code to a file named "room-change.html"
with open( 'טבלת שיבוץ חדרים ראשונית.html', 'w', encoding="utf-8") as f:
    f.write(start_code)
    f.write(json.dumps(data ,ensure_ascii=False))
    f.write(end_code)