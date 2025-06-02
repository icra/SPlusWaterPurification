"""
Model exported as python.
Name : Water purification (landscape)
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


class WaterPurificationLandscape(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterNumber('actualisationrate', 'Actualisation rate', type=QgsProcessingParameterNumber.Double, defaultValue=0.03))
        self.addParameter(QgsProcessingParameterNumber('lifeexpectancyyears', 'Life expectancy (years)', type=QgsProcessingParameterNumber.Double, defaultValue=50))
        self.addParameter(QgsProcessingParameterNumber('ntop', 'Nº of selected top values for mean', type=QgsProcessingParameterNumber.Integer, defaultValue=3, minValue=1))
        self.addParameter(QgsProcessingParameterFile('lsus2', 'Lanscape units layer (lsus2)', behavior=QgsProcessingParameterFile.File, fileFilter='All Files (*.*)', defaultValue='C:\\Users\\xgarcia\\ICRA\\EU MERLIN - Documents\\WP3_upscaling\\SWAT+\\2_Case_study_Scotland_Forth_catchment\\0-Model\\Forth_base_4\\Watershed\\Shapes\\lsus2.shp'))
        self.addParameter(QgsProcessingParameterFile('rivs1', 'Channel layer (rivs1)', behavior=QgsProcessingParameterFile.File, fileFilter='All Files (*.*)', defaultValue='C:\\Users\\xgarcia\\ICRA\\EU MERLIN - Documents\\WP3_upscaling\\SWAT+\\2_Case_study_Scotland_Forth_catchment\\0-Model\\Forth_base_4\\Watershed\\Shapes\\rivs1.shp'))
        self.addParameter(QgsProcessingParameterFile('sqlitebs', 'Sqlite (baseline scenario)', behavior=QgsProcessingParameterFile.File, fileFilter='All Files (*.*)', defaultValue='C:\\Users\\xgarcia\\ICRA\\EU MERLIN - Documents\\WP3_upscaling\\SWAT+\\2_Case_study_Scotland_Forth_catchment\\0-Model\\Forth_base_4\\Scenarios\\Default\\TxtInOut_cal_bau\\nutBAU.sqlite'))
        self.addParameter(QgsProcessingParameterFile('sqliters', 'Sqlite (restoration scenario)', behavior=QgsProcessingParameterFile.File, fileFilter='All Files (*.*)', defaultValue='C:\\Users\\xgarcia\\ICRA\\EU MERLIN - Documents\\WP3_upscaling\\SWAT+\\2_Case_study_Scotland_Forth_catchment\\0-Model\\Forth_base_4\\Scenarios\\Default\\TxtInOut_cal_fullpeat\\nutREST.sqlite'))
        self.addParameter(QgsProcessingParameterNumber('yearlyoperationmaintenancecosteurosha', 'Yearly operation maintenance cost (Euros/ha)', type=QgsProcessingParameterNumber.Double, defaultValue=3850))
        self.addParameter(QgsProcessingParameterFeatureSink('Nitropurval_land', 'NitroPurVal_land', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Phoshpurval_land', 'PhoshPurVal_land', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
        #self.addParameter(QgsProcessingParameterFeatureSink('Dfrgsergtset', 'dfrgsergtset', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(48, model_feedback)
        results = {}
        outputs = {}

        # Join attributes by nearest - Channel
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELDS_TO_COPY': ['Channel'],
            'INPUT': parameters['lsus2'],
            'INPUT_2': parameters['rivs1'],
            'MAX_DISTANCE': None,
            'NEIGHBORS': 1,
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByNearestChannel'] = processing.run('native:joinbynearest', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Extract by expression - rep n
        alg_params = {
            'EXPRESSION': 'n = 1',
            'INPUT': outputs['JoinAttributesByNearestChannel']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtractByExpressionRepN'] = processing.run('native:extractbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # String concatenation channel_sd_monBS
        alg_params = {
            'INPUT_1': parameters['sqlitebs'],
            'INPUT_2': '|layername=channel_sd_mon'
        }
        outputs['StringConcatenationChannel_sd_monbs'] = processing.run('native:stringconcatenation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # String concatenation - lsunit_nb_monBS
        alg_params = {
            'INPUT_1': parameters['sqlitebs'],
            'INPUT_2': '|layername=lsunit_nb_mon'
        }
        outputs['StringConcatenationLsunit_nb_monbs'] = processing.run('native:stringconcatenation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # String concatenation - lsunit_wb_monBS
        alg_params = {
            'INPUT_1': parameters['sqlitebs'],
            'INPUT_2': '|layername=lsunit_wb_mon'
        }
        outputs['StringConcatenationLsunit_wb_monbs'] = processing.run('native:stringconcatenation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # String concatenation - lsunit_ls_monBS
        alg_params = {
            'INPUT_1': parameters['sqlitebs'],
            'INPUT_2': '|layername=lsunit_ls_mon'
        }
        outputs['StringConcatenationLsunit_ls_monbs'] = processing.run('native:stringconcatenation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # String concatenation - lsunit_ls_monRS
        alg_params = {
            'INPUT_1': parameters['sqliters'],
            'INPUT_2': '|layername=lsunit_ls_mon'
        }
        outputs['StringConcatenationLsunit_ls_monrs'] = processing.run('native:stringconcatenation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # String concatenation - lsunit_wb_monRS
        alg_params = {
            'INPUT_1': parameters['sqliters'],
            'INPUT_2': '|layername=lsunit_wb_mon'
        }
        outputs['StringConcatenationLsunit_wb_monrs'] = processing.run('native:stringconcatenation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # String concatenation - lsunit_nb_monRS
        alg_params = {
            'INPUT_1': parameters['sqliters'],
            'INPUT_2': '|layername=lsunit_nb_mon'
        }
        outputs['StringConcatenationLsunit_nb_monrs'] = processing.run('native:stringconcatenation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Field calculator - idmonc channel BS
        alg_params = {
            'FIELD_LENGTH': 30,
            'FIELD_NAME': 'idmonc',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': "concat(yr,'_',mon,'_',gis_id)",
            'INPUT': outputs['StringConcatenationChannel_sd_monbs']['CONCATENATION'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorIdmoncChannelBs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Field calculator - idmon wb BS
        alg_params = {
            'FIELD_LENGTH': 30,
            'FIELD_NAME': 'idmon',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': "concat(yr,'_',mon,'_',(to_real(right(name, 4))/10))",
            'INPUT': outputs['StringConcatenationLsunit_wb_monbs']['CONCATENATION'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorIdmonWbBs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Field calculator - idmon ls RS
        alg_params = {
            'FIELD_LENGTH': 30,
            'FIELD_NAME': 'idmon',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': "concat(yr,'_',mon,'_',(to_real(right(name, 4))/10))",
            'INPUT': outputs['StringConcatenationLsunit_ls_monrs']['CONCATENATION'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorIdmonLsRs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # Field calculator - idmon wb RS
        alg_params = {
            'FIELD_LENGTH': 30,
            'FIELD_NAME': 'idmon',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': "concat(yr,'_',mon,'_',(to_real(right(name, 4))/10))",
            'INPUT': outputs['StringConcatenationLsunit_wb_monrs']['CONCATENATION'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorIdmonWbRs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Field calculator - idmon nb RS
        alg_params = {
            'FIELD_LENGTH': 30,
            'FIELD_NAME': 'idmon',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': "concat(yr,'_',mon,'_',(to_real(right(name, 4))/10))",
            'INPUT': outputs['StringConcatenationLsunit_nb_monrs']['CONCATENATION'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorIdmonNbRs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Field calculator - idmon nb BS
        alg_params = {
            'FIELD_LENGTH': 30,
            'FIELD_NAME': 'idmon',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': "concat(yr,'_',mon,'_',(to_real(right(name, 4))/10))",
            'INPUT': outputs['StringConcatenationLsunit_nb_monbs']['CONCATENATION'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorIdmonNbBs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Field calculator - idmon ls BS
        alg_params = {
            'FIELD_LENGTH': 30,
            'FIELD_NAME': 'idmon',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': "concat(yr,'_',mon,'_',(to_real(right(name, 4))/10))",
            'INPUT': outputs['StringConcatenationLsunit_ls_monbs']['CONCATENATION'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorIdmonLsBs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value - qin RS
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'idmon',
            'FIELDS_TO_COPY': ['precip','wateryld'],
            'FIELD_2': 'idmon',
            'INPUT': outputs['FieldCalculatorIdmonNbRs']['OUTPUT'],
            'INPUT_2': outputs['FieldCalculatorIdmonWbRs']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValueQinRs'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value - qout RS
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'idmon',
            'FIELDS_TO_COPY': ['wateryld'],
            'FIELD_2': 'idmon',
            'INPUT': outputs['FieldCalculatorIdmonLsRs']['OUTPUT'],
            'INPUT_2': outputs['FieldCalculatorIdmonWbRs']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValueQoutRs'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # Field calculator - CNin RS
        alg_params = {
            'FIELD_LENGTH': 13,
            'FIELD_NAME': 'CNin',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': '(grzn + fertn + no3atmo / (14 + 3 * 16) * 14 + nh4atmo / (14 + 4 * 1) * 14)/wateryld*100',
            'INPUT': outputs['JoinAttributesByFieldValueQinRs']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorCninRs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value - qout BS
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'idmon',
            'FIELDS_TO_COPY': ['wateryld'],
            'FIELD_2': 'idmon',
            'INPUT': outputs['FieldCalculatorIdmonLsBs']['OUTPUT'],
            'INPUT_2': outputs['FieldCalculatorIdmonWbBs']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValueQoutBs'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        # Field calculator - CPin RS
        alg_params = {
            'FIELD_LENGTH': 13,
            'FIELD_NAME': 'CPin',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': '(grzp + fertp)/wateryld*100',
            'INPUT': outputs['FieldCalculatorCninRs']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorCpinRs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(21)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value - qin BS
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'idmon',
            'FIELDS_TO_COPY': ['precip','wateryld'],
            'FIELD_2': 'idmon',
            'INPUT': outputs['FieldCalculatorIdmonNbBs']['OUTPUT'],
            'INPUT_2': outputs['FieldCalculatorIdmonWbBs']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValueQinBs'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(22)
        if feedback.isCanceled():
            return {}

        # Field calculator - CNout RS
        alg_params = {
            'FIELD_LENGTH': 13,
            'FIELD_NAME': 'CNout',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': '(sedorgn + surqno3 + lat3no3 + tileno3 + satexn)/wateryld*100',
            'INPUT': outputs['JoinAttributesByFieldValueQoutRs']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorCnoutRs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(23)
        if feedback.isCanceled():
            return {}

        # Field calculator - CNout BS
        alg_params = {
            'FIELD_LENGTH': 20,
            'FIELD_NAME': 'CNout',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': '(sedorgn + surqno3 + lat3no3 + tileno3 + satexn)/wateryld*100',
            'INPUT': outputs['JoinAttributesByFieldValueQoutBs']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorCnoutBs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(24)
        if feedback.isCanceled():
            return {}

        # Field calculator - CNin BS
        alg_params = {
            'FIELD_LENGTH': 20,
            'FIELD_NAME': 'CNin',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': '(grzn + fertn + no3atmo / (14 + 3 * 16) * 14 + nh4atmo / (14 + 4 * 1) * 14)/wateryld*100',
            'INPUT': outputs['JoinAttributesByFieldValueQinBs']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorCninBs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(25)
        if feedback.isCanceled():
            return {}

        # Field calculator - CPout RS
        alg_params = {
            'FIELD_LENGTH': 13,
            'FIELD_NAME': 'CPout',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': '(sedorgp + surqsolp + sedminp + tilelabp)/ wateryld*100',
            'INPUT': outputs['FieldCalculatorCnoutRs']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorCpoutRs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(26)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value - C out RS
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'idmon',
            'FIELDS_TO_COPY': ['CNout','CPout'],
            'FIELD_2': 'idmon',
            'INPUT': outputs['FieldCalculatorCpinRs']['OUTPUT'],
            'INPUT_2': outputs['FieldCalculatorCpoutRs']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValueCOutRs'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(27)
        if feedback.isCanceled():
            return {}

        # Field calculator - CPin BS
        alg_params = {
            'FIELD_LENGTH': 20,
            'FIELD_NAME': 'CPin',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': '(grzp + fertp)/wateryld*100',
            'INPUT': outputs['FieldCalculatorCninBs']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorCpinBs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(28)
        if feedback.isCanceled():
            return {}

        # Field calculator - CPout BS
        alg_params = {
            'FIELD_LENGTH': 20,
            'FIELD_NAME': 'CPout',
            'FIELD_PRECISION': 10,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': '(sedorgp + surqsolp + sedminp + tilelabp)/ wateryld*100',
            'INPUT': outputs['FieldCalculatorCnoutBs']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorCpoutBs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(29)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value - C out BS
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'idmon',
            'FIELDS_TO_COPY': ['wateryld','CNout','CPout'],
            'FIELD_2': 'idmon',
            'INPUT': outputs['FieldCalculatorCpinBs']['OUTPUT'],
            'INPUT_2': outputs['FieldCalculatorCpoutBs']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValueCOutBs'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(30)
        if feedback.isCanceled():
            return {}

        # Field calculator - LSUID
        alg_params = {
            'FIELD_LENGTH': 30,
            'FIELD_NAME': 'LSUID',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 1,  # Integer (32 bit)
            'FORMULA': 'to_real(right(name, 4))',
            'INPUT': outputs['JoinAttributesByFieldValueCOutBs']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorLsuid'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(31)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value - Channel_2
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'LSUID',
            'FIELDS_TO_COPY': ['Area','Channel_2'],
            'FIELD_2': 'LSUID',
            'INPUT': outputs['FieldCalculatorLsuid']['OUTPUT'],
            'INPUT_2': outputs['ExtractByExpressionRepN']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValueChannel_2'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(32)
        if feedback.isCanceled():
            return {}

        # Field calculator - idmonc channel_2 BS
        alg_params = {
            'FIELD_LENGTH': 30,
            'FIELD_NAME': 'idmonc',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Text (string)
            'FORMULA': "concat(yr,'_',mon,'_',Channel_2)",
            'INPUT': outputs['JoinAttributesByFieldValueChannel_2']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorIdmoncChannel_2Bs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(33)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value - water_temp
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'idmonc',
            'FIELDS_TO_COPY': ['water_temp'],
            'FIELD_2': 'idmonc',
            'INPUT': outputs['FieldCalculatorIdmoncChannel_2Bs']['OUTPUT'],
            'INPUT_2': outputs['FieldCalculatorIdmoncChannelBs']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': None,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValueWater_temp'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(34)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value - CNPRest
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'idmon',
            'FIELDS_TO_COPY': ['CNin','CPin','CNout','CPout'],
            'FIELD_2': 'idmon',
            'INPUT': outputs['JoinAttributesByFieldValueWater_temp']['OUTPUT'],
            'INPUT_2': outputs['JoinAttributesByFieldValueCOutRs']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': 'R',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValueCnprest'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(35)
        if feedback.isCanceled():
            return {}

        # Field calculator - CWANBS
        alg_params = {
            'FIELD_LENGTH': 13,
            'FIELD_NAME': 'CWANBS',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': 'case\r\nwhen CNin = 0 then 0\r\nelse\r\n(12 * wateryld * Area / 10 * ln(CNin/CNout)/(30.6*1.102^(water_temp-20)))\r\nend',
            'INPUT': outputs['JoinAttributesByFieldValueCnprest']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorCwanbs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(36)
        if feedback.isCanceled():
            return {}

        # Field calculator - CWAPBS
        alg_params = {
            'FIELD_LENGTH': 13,
            'FIELD_NAME': 'CWAPBS',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': 'case\r\nwhen CPin = 0 then 0\r\nelse\r\n(12 * wateryld * Area / 10 * ln(CPin/CPout)/(30.6*1.102^(water_temp-20))) \r\nend',
            'INPUT': outputs['FieldCalculatorCwanbs']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorCwapbs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(37)
        if feedback.isCanceled():
            return {}

        # Field calculator - CWANRS
        alg_params = {
            'FIELD_LENGTH': 13,
            'FIELD_NAME': 'CWANRS',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': 'case\r\nwhen RCNin = 0 then 0\r\nelse\r\n(12 * wateryld * Area / 10 * ln(RCNin/RCNout)/(30.6*1.102^(water_temp-20)))\r\nEND',
            'INPUT': outputs['FieldCalculatorCwapbs']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorCwanrs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(38)
        if feedback.isCanceled():
            return {}

        # Field calculator - CWAPRS
        alg_params = {
            'FIELD_LENGTH': 13,
            'FIELD_NAME': 'CWAPRS',
            'FIELD_PRECISION': 2,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': 'case\r\nwhen RCPin = 0 then 0\r\nelse\r\n(12 * wateryld * Area / 10 * ln(RCPin/RCPout)/(30.6*1.102^(water_temp-20)))\r\nend',
            'INPUT': outputs['FieldCalculatorCwanrs']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['FieldCalculatorCwaprs'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(39)
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

        feedback.setCurrentStep(40)
        if feedback.isCanceled():
            return {}

        # --- NEW · Rank per LSUID (1,2,3...) ordenat per PCWAinc DESC ---
        outputs['RankPcwa'] = processing.run(
            'native:addautoincrementalfield',
            {
                'INPUT'          : outputs['FieldCalculatorPcwainc']['OUTPUT'],
                'FIELD_NAME'     : 'rank',
                'START'          : 1,
                'GROUP_FIELDS'   : ['LSUID'],        # reinicia a cada LSU
                'SORT_EXPRESSION': '"PCWAinc" DESC', # majors primer
                'OUTPUT'         : QgsProcessing.TEMPORARY_OUTPUT
            },
            context=context, feedback=feedback, is_child_algorithm=True)

        # --- NEW · Quedar-nos només amb els X primers (ntop) ---
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
            'CATEGORIES_FIELD_NAME': ['LSUID'],
            'INPUT': outputs['TopNPcwa']['OUTPUT'],
            'VALUES_FIELD_NAME': 'PCWAinc',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['StatisticsByCategoriesPcwa'] = processing.run('qgis:statisticsbycategories', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        #results['Dfrgsergtset'] = outputs['StatisticsByCategoriesPcwa']['OUTPUT']

        feedback.setCurrentStep(41)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value - PCWA max
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'LSUID',
            'FIELDS_TO_COPY': ['mean'],
            'FIELD_2': 'LSUID',
            'INPUT': parameters['lsus2'],
            'INPUT_2': outputs['StatisticsByCategoriesPcwa']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': 'PCWA_',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValuePcwaMax'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(42)
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

        feedback.setCurrentStep(43)
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

        feedback.setCurrentStep(44)
        if feedback.isCanceled():
            return {}

        rate      = parameters['actualisationrate']                    # 0.03
        life      = parameters['lifeexpectancyyears']                  # 50
        om_cost   = parameters['yearlyoperationmaintenancecosteurosha']# 3850

        expr_phosh = (
            f"(149.34 * (PCWA_mean/10000) ^ 0.69 * 1000) * "
            f"({rate} * (1 + {rate}) ^ {life}) / "
            f"((1 + {rate}) ^ ({life} - 1)) + "
            f"{om_cost} * (PCWA_mean / 10000)"
        )

        # Field calculator - PhoshPurVal
        alg_params = {
            'FIELD_LENGTH': 13,
            'FIELD_NAME': 'PhoshPurVal',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA' : expr_phosh,
            #'FORMULA': '(149.34 * (PCWA_mean/10000)^0.69 *1000)* (@actualisationrate * (1 + @actualisationrate )^ @lifeexpectancyyears )/((1+ @actualisationrate )^(@lifeexpectancyyears - 1)) +   @yearlyoperationmaintenancecosteurosha *(PCWA_mean/10000)',
            'INPUT': outputs['JoinAttributesByFieldValuePcwaMax']['OUTPUT'],
            'OUTPUT': parameters['Phoshpurval_land']
        }
        outputs['FieldCalculatorPhoshpurval'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Phoshpurval_land'] = outputs['FieldCalculatorPhoshpurval']['OUTPUT']

        feedback.setCurrentStep(45)
        if feedback.isCanceled():
            return {}


        # --- NEW · Rank per LSUID (1,2,3...) ordenat per PCWAinc DESC ---
        outputs['RankNcwa'] = processing.run(
            'native:addautoincrementalfield',
            {
                'INPUT'          : outputs['FieldCalculatorNcwainc']['OUTPUT'],
                'FIELD_NAME'     : 'rank',
                'START'          : 1,
                'GROUP_FIELDS'   : ['LSUID'],        # reinicia a cada LSU
                'SORT_EXPRESSION': '"NCWAinc" DESC', # majors primer
                'OUTPUT'         : QgsProcessing.TEMPORARY_OUTPUT
            },
            context=context, feedback=feedback, is_child_algorithm=True)

        # --- NEW · Quedar-nos només amb els X primers (ntop) ---
        outputs['TopNPcwa'] = processing.run(
            'native:extractbyexpression',
            {
                'INPUT'     : outputs['RankNcwa']['OUTPUT'],
                'EXPRESSION': f'"rank" <= {parameters["ntop"]}',
                'OUTPUT'    : QgsProcessing.TEMPORARY_OUTPUT
            },
            context=context, feedback=feedback, is_child_algorithm=True)

        # Statistics by categories - NCWA
        alg_params = {
            'CATEGORIES_FIELD_NAME': ['LSUID'],
            'INPUT': outputs['TopNPcwa']['OUTPUT'],
            'VALUES_FIELD_NAME': 'NCWAinc',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['StatisticsByCategoriesNcwa'] = processing.run('qgis:statisticsbycategories', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(46)
        if feedback.isCanceled():
            return {}

        # Join attributes by field value - NCWA max
        alg_params = {
            'DISCARD_NONMATCHING': False,
            'FIELD': 'LSUID',
            'FIELDS_TO_COPY': ['mean'],
            'FIELD_2': 'LSUID',
            'INPUT': parameters['lsus2'],
            'INPUT_2': outputs['StatisticsByCategoriesNcwa']['OUTPUT'],
            'METHOD': 1,  # Take attributes of the first matching feature only (one-to-one)
            'PREFIX': 'NCWA_',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['JoinAttributesByFieldValueNcwaMax'] = processing.run('native:joinattributestable', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(47)
        if feedback.isCanceled():
            return {}


        rate    = parameters['actualisationrate']
        life    = parameters['lifeexpectancyyears']
        om_cost = parameters['yearlyoperationmaintenancecosteurosha']

        expr_nitro = (
            f"(149.34 * (NCWA_mean/10000) ^ 0.69 * 1000) * "
            f"({rate} * (1 + {rate}) ^ {life}) / "
            f"((1 + {rate}) ^ ({life} - 1)) + "
            f"{om_cost} * (NCWA_mean / 10000)"
        )

        # Field calculator - NitroPurVal
        alg_params = {
            'FIELD_LENGTH': 13,
            'FIELD_NAME': 'NitroPurVal',
            'FIELD_PRECISION': 3,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': expr_nitro,
            #'FORMULA': '(149.34 * (NCWA_max/10000)^0.69 *1000)* (@actualisationrate * (1 + @actualisationrate )^ @lifeexpectancyyears )/((1+ @actualisationrate )^(@lifeexpectancyyears - 1)) +   @yearlyoperationmaintenancecosteurosha *(NCWA_max/10000)',
            'INPUT': outputs['JoinAttributesByFieldValueNcwaMax']['OUTPUT'],
            'OUTPUT': parameters['Nitropurval_land']
        }
        outputs['FieldCalculatorNitropurval'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Nitropurval_land'] = outputs['FieldCalculatorNitropurval']['OUTPUT']
        return results

    def name(self):
        return 'Water purification (landscape)'

    def displayName(self):
        return 'Water purification (landscape)'

    def group(self):
        return 'MERLIN'

    def groupId(self):
        return 'MERLIN'

    def createInstance(self):
        return WaterPurificationLandscape()
