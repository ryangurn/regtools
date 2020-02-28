"""
ClassParser.py this is the file that allows us to quickly query the data source:
classes.uoregon.edu

Authors:
(RegTools)
Joseph Goh
Mason Sayyadi
Owen McEvoy
Ryan Gurnick
Samuel Lundquist

Priority credit to:
Ryan Gurnick - 2/25/20  Creation

"""
import Parser
import requests


class ClassParser:
    def __init__(self, term: str, subject: str):
        """
        Initializer for the class parser. This will allow a parser to be
        specified that will generate a set of tables in the form of lists
        of lists

        Example Usage:
        p = Parser.Parser()
        parser = ClassParser.Parser("201903", "CIS")
        """
        cis_catalog_url = "http://classes.uoregon.edu/pls/prod/hwskdhnt.P_ListCrse?term_in=" + term + "&sel_subj=dummy&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy&sel_cred=dummy&sel_tuition=dummy&sel_open=dummy&sel_weekend=dummy&sel_title=&sel_to_cred=&sel_from_cred=&sel_subj=" + subject + "&sel_crse=&sel_crn=&sel_camp=%25&sel_levl=%25&sel_attr=%25&begin_hh=0&begin_mi=0&begin_ap=a&end_hh=0&end_mi=0&end_ap=a&submit_btn=Show+Classes"
        catalog = requests.get(cis_catalog_url)

        p = Parser.Parser()
        p.feed(str(catalog.content))

        self.term = term
        self.subject = subject
        self._parser = p
        self._tables = self._parser.tables
        self._intermediateData = None
        self._dict = {}

    def deleteFormatting(self):
        """
        deleteFormatting is here to remove the formatting from the
        table design that is provided by classes.uoregon.edu

        This will remove headers from each course subsection
        This will remove the amount of results from the bottom
        This will remove many empty arrays that are to denote formatting

        This will NOT remove empty arrays or empty strings that denote
        empty fields such as Instructor or Location that are not provided
        for some unknown reason.

        :return:

        Example Usage:
        (Continuation of the __init__ example)

        parser.deleteFormatting()
        """
        del self._tables[:3]  # strip some of the formatting nonsense
        del self._tables[-3:]  # strip some js and empty rows (formatting nonsense)

        # copy data for move to _intermediateData
        ret_arr = []
        for data in self._tables:
            ret_arr.append(data)

        del ret_arr[0][0]
        for key, val in enumerate(ret_arr):
            # skip the zero-th item
            if key != 0:
                # removes headers from the start of each table
                del ret_arr[key][0:3]
                for ret_arr_key, ret_arr_val, in enumerate(ret_arr[key]):
                    if len(ret_arr[key][ret_arr_key]) == 1:
                        del ret_arr[key][ret_arr_key]  # delete empty lists at the end of each row
            elif key == 0:
                # replace some bad formatting
                ret_arr[0][0][0] = ret_arr[0][0][0].replace("Classes Found   ", "", 1)

        # del ret_arr[-1]  # removing the number of classes found
        # for k, v in enumerate(ret_arr):
        #     if len(ret_arr[k]) == 1:
        #         del ret_arr[k]

        self._intermediateData = ret_arr

    def parseData(self):
        for key, val in enumerate(self._intermediateData):
            # init obj
            class_obj =  {
                'subject': '',
                'number': '',
                'name': '',
                'credits': '',
                'grading': '',
                'sections': [],
            }

            # get the name and credits
            if len(self._intermediateData[key-1][-2]) == 2:
                name_info = self._intermediateData[key-1][-2][0].split(" ")
                num = name_info[1]
                sub = name_info[0]
                course_name = ' '.join(name_info[2:]).replace('\u00a0', "")
                class_obj['number'] = num
                class_obj['subject'] = sub
                class_obj['name'] = course_name
                class_obj['credits'] = self._intermediateData[key-1][-2][1]

            # get the grading info
            if len(self._intermediateData[key-1][-1]) == 2:
                class_obj['grading'] = self._intermediateData[key-1][-1][1]

            data = self._intermediateData[key]
            for k, v in enumerate(data):
                item = data[k]
                if len(item) == 9:
                    section_obj = {
                        'type': '',
                        'crn': '',
                        'avail': 0,
                        'max': 0,
                        'taken': 0,
                        'time': '',
                        'day': '',
                        'location': '',
                        'instructor': '',
                        'notes': '',
                        'url': '',
                    }
                    section_obj['type'] = item[0]
                    section_obj['crn'] = item[1]
                    section_obj['avail'] = int(item[2])
                    section_obj['max'] = int(item[3])
                    section_obj['taken'] = int(int(item[3])-int(item[2]))
                    section_obj['time'] = item[4]
                    section_obj['day'] = item[5]
                    section_obj['location'] = item[6]
                    section_obj['instructor'] = item[7]
                    section_obj['notes'] = item[8]
                    section_obj['url'] = "http://classes.uoregon.edu/pls/prod/hwskdhnt.p_viewdetl?term="+self.term+"&crn="+item[1]
                    class_obj['sections'].append(section_obj)

            if class_obj != {'subject': '', 'number': '', 'name': '', 'credits': '', 'grading': '','sections': [],}:
                self._dict.update({
                    str(class_obj['subject'] + " " + class_obj['number'] + " - [" + class_obj['name'] +"]"): class_obj
                })
        print(self._dict)
