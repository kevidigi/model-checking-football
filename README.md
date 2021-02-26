# Model Checking for Strategy Generation in Football

Senior honours project, BSc Software Engineering, University of Glasgow.

Datasets available from: https://figshare.com/collections/Soccer_match_event_dataset/4415000/2

(Pappalardo, L., Cintia, P., Rossi, A. et al.; A public data set of spatio-temporal match events in soccer competitions; Sci Data 6, 236 (2019). https://doi.org/10.1038/s41597-019-0247-7)

To generate models:
* Clone the repository
* Download "events_Italy.json", "events_France.json", "events_Spain.json", "events_Germany.json" and "events_England.json" from the datasets above
* Create a directory in the project root called "data" and place the .json files inside it
* Run "code/python/extract_wyscout_data.py" to generate PRISM files in "code/prism/"
