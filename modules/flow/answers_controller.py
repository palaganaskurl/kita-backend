from typing import List, Dict

import pandas as pd


class AnswersController:
    @staticmethod
    def group_answers_by_psid(answers: List[Dict]):
        grouped_answers = {}

        for answer in answers:
            psid = answer.get('psid')

            question_code = answer.get('question_code')

            # TODO: Temporary for now since single digit
            day_index = 3
            question_index = -1

            day_no = question_code[day_index]
            question_no = question_code[question_index]

            answer['day_no'] = day_no
            answer['question_no'] = question_no

            if psid not in grouped_answers:
                grouped_answers[psid] = [answer]
            else:
                grouped_answers[psid].append(answer)

        return grouped_answers

    @staticmethod
    def grouped_answers_by_day(grouped_answers_by_psid: Dict):
        grouped_answers = {}

        for psid, answers in grouped_answers_by_psid.items():
            grouped_answers[psid] = {}

            for answer in answers:
                day_no = answer['day_no']

                if day_no not in grouped_answers[psid]:
                    grouped_answers[psid][day_no] = [answer]
                else:
                    grouped_answers[psid][day_no].append(answer)

        return grouped_answers

    @staticmethod
    def get_date_started_ended_per_day_per_psid(grouped_answers_by_day: Dict):
        data = []

        for psid, grouped_by_day in grouped_answers_by_day.items():
            for day, answers in grouped_by_day.items():

                __data = {
                    'day': day,
                    'date_started': answers[0]['updated_on'],
                    'date_ended': answers[-1]['updated_on'],
                    'psid': psid
                }

                data.append(__data)

        return list(sorted(data, key=lambda k: k['day']))

    @staticmethod
    def generate_excel(data):
        df = pd.DataFrame(data)

        return df.to_excel('answers.xlsx')
