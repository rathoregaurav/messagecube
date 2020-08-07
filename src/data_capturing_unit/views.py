"""data capturing from csv file
"""
import os

from django.db.models import Avg
from django.db.models import Count
from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView

from data_capturing_unit.models import MessageData
from helper.messages import MESSAGES
from helper.utils import api_response_parser
from messagecube.settings import BASE_DIR
import csv

FILE = os.path.dirname(BASE_DIR)+"/docs/cunique.csv"


class LoadData(APIView):
    """
    api view to load data from csv file into database
    """

    @staticmethod
    def get(_):
        """
        this module load data from csv file into message data models
        :param _:
        :return: api response
        """
        with open(FILE, "r") as file:
            data = csv.reader(file)
            for index, row in enumerate(list(data)[1:]):
                try:
                    MessageData.objects.update_or_create(id=row[0],
                                                        defaults={
                                                            'message': row[1],
                                                            'truth': row[2],
                                                            'cube': row[3],
                                                            'google': row[4],
                                                            'google_spam': row[5],
                                                            'google_not_spam': row[6],
                                                            'ibm': row[7],
                                                            'ibm_spam': row[8],
                                                            'ibm_not_spam': row[9]
                                                        })
                except IndexError:
                    pass
        return api_response_parser(data={},
                                   message=MESSAGES["SUCCESS"],
                                   status=status.HTTP_200_OK,
                                   success=True)



class MessageSearch(APIView):
    """
    generic view to search message
    """
    queryset = MessageData.objects.all()

    @staticmethod
    def parse_result(group_queryset):
        """
        format result data
        :param group_queryset:
        :return:
        """
        formatted_dict = dict()
        _result = dict(group_queryset.aggregate(
            count=Count('id'),
            google_spam_avg=Avg('google_spam'),
            ibm_spam_avg=Avg('ibm_spam'),
            google_not_spam_avg=Avg('google_not_spam'),
            ibm_not_spam_avg=Avg('ibm_not_spam'),
            ibm_spam_count=Count('ibm', filter=Q(ibm='spam')),
            ibm_not_spam_count=Count('ibm', filter=Q(ibm='not-spam')),
            google_spam_count=Count('google', filter=Q(google='spam')),
            google_not_spam_count=Count('google', filter=Q(google='not-spam')),
            truth_spam_count=Count('truth', filter=Q(truth='spam')),
            truth_not_spam_count=Count('truth', filter=Q(truth='not-spam')),
            cube_spam_count=Count('cube', filter=Q(cube='spam')),
            cube_not_spam_count=Count('cube', filter=Q(cube='not-spam'))
        ))

        formatted_dict["total_matches"] = _result['count']

        formatted_dict["truth"] = dict((k, _result[k]) for k in _result.keys()
                                       if k in ['truth_spam_count', 'truth_not_spam_count'])

        formatted_dict["cube"] = dict((k, _result[k]) for k in _result.keys()
                                       if k in ['cube_spam_count', 'cube_not_spam_count'])

        formatted_dict["google"] = dict((k, _result[k]) for k in _result.keys()
                                       if k in ['google_spam_avg', 'google_not_spam_avg',
                                                'google_spam_count', 'google_not_spam_count'])

        formatted_dict["ibm"] = dict((k, _result[k]) for k in _result.keys()
                                       if k in ['ibm_spam_avg', 'ibm_not_spam_avg',
                                                'ibm_spam_count', 'ibm_not_spam_count'])

        return formatted_dict


    def get(self, _):
        """
        url: /api/v1/search/?query=<>
        :return: json response
        """
        search_param = self.request.query_params.get('query')
        if not search_param:
            group_queryset = self.queryset.all()
        else:
            group_queryset = self.queryset.filter(message__icontains=search_param.strip())
        return api_response_parser(data=self.parse_result(group_queryset),
                                   message=MESSAGES["SUCCESS"],
                                   status=status.HTTP_200_OK,
                                   success=True)
