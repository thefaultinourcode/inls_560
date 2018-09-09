# Assignment 6: Create a Google column chart using the JSON data produced by the web api:
#  http://hive2.cci.drexel.edu:8080/generateIndex?url=https://en.wikipedia.org/wiki/Geology&vocs=USGS,UAT
import urllib.request
import urllib.error
from urllib.error import URLError, HTTPError
import json
import webbrowser
import gviz_api

# HTML template with embedded JavaScript that creates the Google column chart
column_template = """
<html>
  <head>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = new google.visualization.DataTable(%(json_text)s);

        var options = {
          title: 'USGS and UAT Vocabulary Concepts in Geology Wiki',
          colors: ['chocolate']
        };

        var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
    <div id="chart_div" style="width: 100em; height: 37.5em;"></div>
  </body>
</html>
"""

# Create the HTML output file, call extract_data to process the JSON to populate the chart,
#   and display the HTML in the browser.
# Note: if the webbrowser module does not work in your environment, you can test by opening the
#   generated HTML file in your browser.
def main():
    filename = 'google_chart.html'
    try:
        html_file = open(filename, 'w', encoding='utf8')
        extract_data(html_file, filename)
        html_file.close()

        webbrowser.open_new_tab(filename)   # Open the HTML file in a browser
    except FileNotFoundError as err:
        print('Error: cannot find file,', filename)
        print(err)
    except OSError as err:
        print('Error: cannot access file,', filename)
        print(err)
    except Exception as err:
        print('Error:', err)


def extract_data(html_file, filename):
    try:
        # Call the web api and save the returned JSON data in the index_content variable
        index_url = "http://hive2.cci.drexel.edu:8080/generateIndex?url=https://en.wikipedia.org/wiki/Geology&vocs=USGS,UAT"
        index_content = urllib.request.urlopen(index_url).read().decode('utf8')

        # If you cannot read the url w/o an exception being raised, use the provided file, hive_index.json
        # input_file = open('hive_index.json', 'r', encoding="utf8")
        # index_content = input_file.read()
        # input_file.close()

        # Parse the json data.
        index_list = json.loads(index_content)
        data = []

        # Extract the voc, prefLabel, and score data for the chart
        # The data variable should define a list of tuples where
        #   each tuple defines a concept and its score, e.g., ('erosion (USGS)', 1.2)

        # iterate through the items in index_list
        for item in index_list:
            # store the vocabulary for each item in a variable
            voc = item['voc']

            # iterate through the concept dictionary to get the prefLabel and score
            concepts = item['concepts']
            for concept in concepts:
                prefLabel = concept['prefLabel']
                score = concept['score']
                # concatenate the prefLabel with voc to make labels
                concept_defintion = prefLabel + " (" + voc + ")"
                # add tuple from this iteration to the list of data
                data.append((concept_defintion, float(score)))

        # Create the schema for the Google DataTable by defining the columns and their types
        description = [("Concept", "string"), ("Score", "number")]

        # Use the Google Python library, gvis_api, to create and load the DataTable object
        data_table = gviz_api.DataTable(description)
        data_table.LoadData(data)

        # Convert to JSON format that Google charts requires
        json_text = data_table.ToJSon()

        # Write the column_template to the file
        html_file.write(column_template % vars())
    except ValueError as err:
        print('An error occurred trying to decode the json text')
        print(err)
    except FileNotFoundError as err:
        print('Unable to find file,', filename)
        print(err)
    except HTTPError as err:
        print('Server could not fulfill the request.')
        print(err)
    except URLError as err:
        print('Failed to reach a server.')
        print(err)
    except OSError as err:
        print('Unable to access file,', filename)
        print(err)
    except Exception as err:
        print('An error occurred: ', err)


main()
