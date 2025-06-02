"""
Model exported as python.
Name : Water purification (channel)
Group : MERLIN
With QGIS : 34006
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterFile
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsExpression
import processing


class WaterPurificationChannel(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterNumber('actualisationrate', 'Actualisation rate', type=QgsProcessingParameterNumber.Double, defaultValue=0.03))
        self.addParameter(QgsProcessingParameterNumber('life_expectancy_years', 'Life expectancy (years)', type=QgsProcessingParameterNumber.Double, defaultValue=20))
        self.addParameter(QgsProcessingParameterNumber('ntop','Nº of selected top values for mean', type=QgsProcessingParameterNumber.Integer, defaultValue=3, minValue=1))
        self.addParameter(QgsProcessingParameterFile('rivs1', 'Channels layer (rivs1)', behavior=QgsProcessingParameterFile.File, fileFilter='All Files (*.*)', defaultValue='C:\\Users\\xgarcia\\ICRA\\EU MERLIN - Documents\\WP3_upscaling\\SWAT+\\2_Case_study_Scotland_Forth_catchment\\0-Model\\Forth_base_4\\Watershed\\Shapes\\rivs1.shp'))
        self.addParameter(QgsProcessingParameterFile('sqlitebs', 'Sqlite (baseline scenario)', behavior=QgsProcessingParameterFile.File, fileFilter='All Files (*.*)', defaultValue='C:\\Users\\xgarcia\\ICRA\\EU MERLIN - Documents\\WP3_upscaling\\SWAT+\\2_Case_study_Scotland_Forth_catchment\\0-Model\\Forth_base_4\\Scenarios\\Default\\TxtInOut_cal_bau\\nutBAU.sqlite'))
        self.addParameter(QgsProcessingParameterFile('sqliters', 'Sqlite (restoration scenario)', behavior=QgsProcessingParameterFile.File, fileFilter='All Files (*.*)', defaultValue='C:\\Users\\xgarcia\\ICRA\\EU MERLIN - Documents\\WP3_upscaling\\SWAT+\\2_Case_study_Scotland_Forth_catchment\\0-Model\\Forth_base_4\\Scenarios\\Default\\TxtInOut_cal_fullpeat\\nutREST.sqlite'))
        self.addParameter(QgsProcessingParameterNumber('yearlyoperationmaintenancecosteurosha', 'Yearly operation maintenance cost (Euros/ha)', type=QgsProcessingParameterNumber.Double, defaultValue=3850))
        self.addParameter(QgsProcessingParameterFeatureSink('Nitropurval_channel', 'NitroPurVal_channel', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Phoshpurval_channel', 'PhoshPurVal_channel', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(25, model_feedback)
        results = {}
        outputs = {}

        # String concatenation - channel_sd_monBS
        alg_params = {
            'INPUT_1': parameters['sqlitebs'],
            'INPUT_2': '|layername=channel_sd_mon'
        }
        outputs['StringConcatenationChannel_sd_monbs'] = processing.run('native:stringconcatenation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # String concatenation - channel_sd_monRS
        alg_params = {
            'INPUT_1': parameters['sqliters'],
            'INPUT_2': '|layername=channel_sd_mon'
        }
        outputs['StringConcatenationChannel_sd_monrs'] = processing.run('native:stringconcatenation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Field calculator - idmon channel RS
        alg_params = {
            'FIELD_LENGTH': 30,
            'FIELD_NAME': 'idmon',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': "concat(yr,'_',mon,'_',gis_id)",
            'INPUT': outputs['StringConcatenationChannel_sd_monrs']['CONCATENATION'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorIdmonChannelRs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Field calculator - idmon channel BS
        alg_params = {
            'FIELD_LENGTH': 30,
            'FIELD_NAME': 'idmon',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': "concat(yr,'_',mon,'_',gis_id)",
            'INPUT': outputs['StringConcatenationChannel_sd_monbs']['CONCATENATION'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorIdmonChannelBs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Field calculator - CNin BS
        alg_params = {
            'FIELD_LENGTH': 13,
            'FIELD_NAME': 'CNin',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': '(orgn_in + no3_in + nh3_in + no2_in)/ (flo_in * 60 * 60 * 24 * 30.5) * 1000',
            'INPUT': outputs['FieldCalculatorIdmonChannelBs']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorCninBs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Field calculator - CNin RS
        alg_params = {
            'FIELD_LENGTH': 13,
            'FIELD_NAME': 'CNin',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': '(orgn_in + no3_in + nh3_in + no2_in)/ (flo_in * 60 * 60 * 24 * 30.5) * 1000',
            'INPUT': outputs['FieldCalculatorIdmonChannelRs']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorCninRs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Field calculator - CPin RS
        alg_params = {
            'FIELD_LENGTH': 13,
            'FIELD_NAME': 'CPin',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': '(sedp_in + solp_in)/ (flo_in * 60 * 60 * 24 * 30.5) * 1000',
            'INPUT': outputs['FieldCalculatorCninRs']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorCpinRs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Field calculator - CPin BS
        alg_params = {
            'FIELD_LENGTH': 13,
            'FIELD_NAME': 'CPin',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': '(sedp_in + solp_in)/ (flo_in * 60 * 60 * 24 * 30.5) * 1000',
            'INPUT': outputs['FieldCalculatorCninBs']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorCpinBs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Field calculator - CNout BS
        alg_params = {
            'FIELD_LENGTH': 13,
            'FIELD_NAME': 'CNout',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': '(orgn_out + no3_out + nh3_out + no2_out)/ (flo_out * 60 * 60 * 24 * 30.5) * 1000',
            'INPUT': outputs['FieldCalculatorCpinBs']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorCnoutBs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Field calculator - CNout RS
        alg_params = {
            'FIELD_LENGTH': 13,
            'FIELD_NAME': 'CNout',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': '(orgn_out + no3_out + nh3_out + no2_out)/ (flo_out * 60 * 60 * 24 * 30.5) * 1000',
            'INPUT': outputs['FieldCalculatorCpinRs']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorCnoutRs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Field calculator - CPout BS
        alg_params = {
            'FIELD_LENGTH': 13,
            'FIELD_NAME': 'CPout',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': '(sedp_out + solp_out)/ (flo_out * 60 * 60 * 24 * 30.5) * 1000',
            'INPUT': outputs['FieldCalculatorCnoutBs']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorCpoutBs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Field calculator - CPout RS
        alg_params = {
            'FIELD_LENGTH': 13,
            'FIELD_NAME': 'CPout',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': '(sedp_out + solp_out)/ (flo_out * 60 * 60 * 24 * 30.5) * 1000',
            'INPUT': outputs['FieldCalculatorCnoutRs']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorCpoutRs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value - CNPRest
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'idmon',
            'FIELDS_TO_COPY': ['CNin','CPin','CNout','CPout'],
            'FIELD_2': 'idmon',
            'INPUT': outputs['FieldCalculatorCpoutBs']['OUTPUT'],
            'INPUT_2': outputs['FieldCalculatorCpoutRs']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': 'R',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValueCnprest'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Field calculator - CWANBS
        alg_params = {
            'FIELD_LENGTH': 13,
            'FIELD_NAME': 'CWANBS',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': '\r\ncase\r\nwhen CNin = 0 then 0\r\nelse\r\n(12 * (flo_out*60*60*24*30.5) / 10 * ln(CNin/CNout)/(30.6*1.102^(water_temp-20)))\r\n end',
            'INPUT': outputs['JoinAttributesByFieldValueCnprest']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorCwanbs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Field calculator - CWAPBS
        alg_params = {
            'FIELD_LENGTH': 13,
            'FIELD_NAME': 'CWAPBS',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': 'case\r\nwhen CPin = 0 then 0\r\nelse\r\n(12 * (flo_out*60*60*24*30.5) / 10 * ln(CPin/CPout)/(30.6*1.102^(water_temp-20))) \r\nend',
            'INPUT': outputs['FieldCalculatorCwanbs']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorCwapbs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Field calculator - CWANRS
        alg_params = {
            'FIELD_LENGTH': 13,
            'FIELD_NAME': 'CWANRS',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': 'case\r\nwhen RCNin = 0 then 0\r\nelse\r\n(12 * (flo_out*60*60*24*30.5) / 10 * ln(RCNin/RCNout)/(30.6*1.102^(water_temp-20)))\r\nend',
            'INPUT': outputs['FieldCalculatorCwapbs']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorCwanrs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Field calculator - CWAPRS
        alg_params = {
            'FIELD_LENGTH': 13,
            'FIELD_NAME': 'CWAPRS',
            'FIELD_PRECISION': 2,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': 'case\r\nwhen RCPin = 0 then 0\r\nelse\r\n(12 * (flo_out*60*60*24*30.5) / 10 * ln(RCPin/RCPout)/(30.6*1.102^(water_temp-20)))\r\nend',
            'INPUT': outputs['FieldCalculatorCwanrs']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorCwaprs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # Field calculator - PCWAinc
        alg_params = {
            'FIELD_LENGTH': 20,
            'FIELD_NAME': 'PCWAinc',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': 'CWAPRS - CWAPBS\r\n',
            'INPUT': outputs['FieldCalculatorCwaprs']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorPcwainc'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # --- Rank PCWA per canal ---------------------------------------------
        outputs['RankPcwa'] = processing.run(
            'native:addautoincrementalfield',
            {
                'INPUT'          : outputs['FieldCalculatorPcwainc']['OUTPUT'],
                'FIELD_NAME'     : 'rank',
                'START'          : 1,
                'GROUP_FIELDS'   : ['gis_id'],      # un rànquing per cada canal
                'SORT_EXPRESSION': '"PCWAinc" DESC',
                'OUTPUT'         : QgsProcessing.TEMPORARY_OUTPUT
            },
            context=context, feedback=feedback, is_child_algorithm=True)

        # --- Quedar-nos amb els X primers (ntop) ------------------------------
        outputs['TopNPcwa'] = processing.run(
            'native:extractbyexpression',
            {
                'INPUT'     : outputs['RankPcwa']['OUTPUT'],
                'EXPRESSION': f'"rank" <= {parameters["ntop"]}',
                'OUTPUT'    : QgsProcessing.TEMPORARY_OUTPUT
            },
            context=context, feedback=feedback, is_child_algorithm=True)

        # Statistics by categories - PCWA
        alg_params = {
            'CATEGORIES_FIELD_NAME': ['gis_id'],
            'INPUT': outputs['TopNPcwa']['OUTPUT'],
            'VALUES_FIELD_NAME': 'PCWAinc',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['StatisticsByCategoriesPcwa'] = processing.run('qgis:statisticsbycategories', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # Field calculator - NCWAinc
        alg_params = {
            'FIELD_LENGTH': 20,
            'FIELD_NAME': 'NCWAinc',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': 'CWANRS - CWANBS\r\n',
            'INPUT': outputs['FieldCalculatorCwaprs']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorNcwainc'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        # --- Rank NCWA per canal ---------------------------------------------
        outputs['RankNcwa'] = processing.run(
            'native:addautoincrementalfield',
            {
                'INPUT'          : outputs['FieldCalculatorNcwainc']['OUTPUT'],
                'FIELD_NAME'     : 'rank',
                'START'          : 1,
                'GROUP_FIELDS'   : ['gis_id'],
                'SORT_EXPRESSION': '"NCWAinc" DESC',
                'OUTPUT'         : QgsProcessing.TEMPORARY_OUTPUT
            },
            context=context, feedback=feedback, is_child_algorithm=True)

        outputs['TopNNcwa'] = processing.run(
            'native:extractbyexpression',
            {
                'INPUT'     : outputs['RankNcwa']['OUTPUT'],
                'EXPRESSION': f'"rank" <= {parameters["ntop"]}',
                'OUTPUT'    : QgsProcessing.TEMPORARY_OUTPUT
            },
            context=context, feedback=feedback, is_child_algorithm=True)


        # Join attributes by field value - PCWA max
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'Channel',
            'FIELDS_TO_COPY': ['mean'],
            'FIELD_2': 'gis_id',
            'INPUT': parameters['rivs1'],
            'INPUT_2': outputs['StatisticsByCategoriesPcwa']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': 'PCWA_',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValuePcwaMax'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(21)
        if feedback.isCanceled():
            return {}

        # Field calculator - PhoshPurVal

        rate    = parameters['actualisationrate']
        life    = parameters['life_expectancy_years']
        om_cost = parameters['yearlyoperationmaintenancecosteurosha']

        expr_phos = (
            "case "
            "when coalesce(PCWA_mean,0) <= 0 then 0 "   
            f"else (149.34 * (PCWA_mean/10000) ^ 0.69 * 1000) * "
            f"({rate} * (1 + {rate}) ^ {life}) / "
            f"((1 + {rate}) ^ ({life} - 1)) + "
            f"{om_cost} * (PCWA_mean / 10000)"
            "end"
        )

        alg_params = {
            'FIELD_LENGTH': 13,
            'FIELD_NAME': 'PhoshPurVal',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': expr_phos,
            #'FORMULA': '(149.34 * (PCWA_max/10000)^0.69 *1000)* (@actualisationrate * (1 + @actualisationrate )^  @life_expectancy_years  )/((1+ @actualisationrate )^( @life_expectancy_years  - 1)) +   @yearlyoperationmaintenancecosteurosha *(PCWA_max/10000)',
            'INPUT': outputs['JoinAttributesByFieldValuePcwaMax']['OUTPUT'],
            'OUTPUT': parameters['Phoshpurval_channel']
        }
        outputs['FieldCalculatorPhoshpurval'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Phoshpurval_channel'] = outputs['FieldCalculatorPhoshpurval']['OUTPUT']

        feedback.setCurrentStep(22)
        if feedback.isCanceled():
            return {}

        # Statistics by categories - NCWA
        alg_params = {
            'CATEGORIES_FIELD_NAME': ['gis_id'],
            'INPUT': outputs['TopNNcwa']['OUTPUT'],
            'VALUES_FIELD_NAME': 'NCWAinc',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['StatisticsByCategoriesNcwa'] = processing.run('qgis:statisticsbycategories', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(23)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value - NCWA max
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'Channel',
            'FIELDS_TO_COPY': ['mean'],
            'FIELD_2': 'gis_id',
            'INPUT': parameters['rivs1'],
            'INPUT_2': outputs['StatisticsByCategoriesNcwa']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': 'NCWA_',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValueNcwaMax'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(24)
        if feedback.isCanceled():
            return {}

        # Field calculator - NitroPurVal

        rate    = parameters['actualisationrate']
        life    = parameters['life_expectancy_years']
        om_cost = parameters['yearlyoperationmaintenancecosteurosha']

        expr_nitro = (
            "case "
            "when coalesce(NCWA_mean,0) <= 0 then 0 "
            f"else (149.34 * (NCWA_mean/10000) ^ 0.69 * 1000) * "
            f"({rate} * (1 + {rate}) ^ {life}) / "
            f"((1 + {rate}) ^ ({life} - 1)) + "
            f"{om_cost} * (NCWA_mean / 10000)"
            "end"
        )

        alg_params = {
            'FIELD_LENGTH': 13,
            'FIELD_NAME': 'NitroPurVal',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': expr_nitro,
            #'FORMULA': '(149.34 * (NCWA_max/10000)^0.69 *1000)* ( @actualisationrate  * (1 +  @actualisationrate )^  @life_expectancy_years  )/((1+ @actualisationrate )^( @life_expectancy_years  - 1)) +    @yearlyoperationmaintenancecosteurosha  *(NCWA_max/10000)',
            'INPUT': outputs['JoinAttributesByFieldValueNcwaMax']['OUTPUT'],
            'OUTPUT': parameters['Nitropurval_channel']
        }
        outputs['FieldCalculatorNitropurval'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Nitropurval_channel'] = outputs['FieldCalculatorNitropurval']['OUTPUT']
        return results

    def name(self):
        return 'Water purification (channel)'

    def displayName(self):
        return 'Water purification (channel)'

    def group(self):
        return 'MERLIN'

    def groupId(self):
        return 'MERLIN'

    def createInstance(self):
        return WaterPurificationChannel()
