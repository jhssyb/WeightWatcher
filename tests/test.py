import unittest
import warnings
warnings.simplefilter(action='ignore', category=RuntimeWarning)

import sys
sys.path.append("C:/Users/mzczm/WeightWatcher")

import weightwatcher as ww

import torchvision.models as models
import pandas as pd

import logging


class Test_VGG11(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		"""I run only once for this class
		"""
		
		cls.model = models.vgg11(pretrained=True)
		cls.watcher = ww.WeightWatcher(model=cls.model, log=False)


	def setUp(self):
		"""I run before every test in this class
		"""
		pass


	def test_summary_is_dict(self):
		"""Test that get_summary() returns a valid python dict
		"""
		self.watcher.analyze()
		summary = self.watcher.get_summary()

		self.assertTrue(isinstance(summary, dict), "Summary is a dictionary")

		for key in ['norm', 'norm_compound', 'lognorm', 'lognorm_compound']:
			self.assertTrue(key in summary, "{} in summary".format(key))


	def test_pandas(self):
		"""Test that get_summary(pandas=True) returns a valid pandas dataframe
		"""
		

		self.watcher.analyze()
		summary = self.watcher.get_summary(pandas=True)

		self.assertEqual(isinstance(summary, pd.DataFrame), True, "Summary is a pandas DataFrame")

		columns = ",".join(summary.columns)
		for key in ['norm', 'norm_compound', 'lognorm', 'lognorm_compound']:
			self.assertTrue(key in summary.columns, "{} in summary. Columns are {}".format(key, columns))


	def test_filter_dense_layer_types(self):
		"""Test that ww.LAYER_TYPE.DENSE filter is applied only to DENSE layers"
		"""

		results = self.watcher.analyze(layers=ww.LAYER_TYPE.DENSE)
		d = self.watcher.get_details(results=results)

		denseLayers = d[d['layer_type']=="DENSE"]
		denseCount = len(denseLayers)

		self.assertTrue(denseCount > 0, "Non zero number of dense layers: {} found".format(denseCount))
			
		# Dense layers are analyzed
		self.assertTrue((denseLayers.N > 0).all(axis=None), "All {} dense layers have a non zero N".format(denseCount))
		self.assertTrue((denseLayers.M > 0).all(axis=None), "All {} dense layers have a non zero M".format(denseCount))

		nonDenseLayers = d[d['layer_type']!="DENSE"]
		nonDenseCount = len(nonDenseLayers)

		self.assertTrue(nonDenseCount > 0, "VGG11 has non dense layers: {} found".format(nonDenseCount))
		
		# Non Dense layers are NOT analyzed
		self.assertTrue((nonDenseLayers.N == 0).all(axis=None), "All {} NON dense layers have a zero N".format(nonDenseCount))
		self.assertTrue((nonDenseLayers.M == 0).all(axis=None), "All {} NON dense layers have a zero M".format(nonDenseCount))


	def test_filter_conv2D_layer_types(self):
		"""Test that ww.LAYER_TYPE.CONV2D filter is applied only to CONV2D layers"
		"""

		results = self.watcher.analyze(layers=ww.LAYER_TYPE.CONV2D)
		d = self.watcher.get_details(results=results)

		conv2DLayers = d[d['layer_type']=="CONV2D"]
		conv2DCount = len(conv2DLayers)

		self.assertTrue(conv2DCount > 0, "Non zero number of conv2D layers: {} found".format(conv2DCount))
			
		# Conv2D layers are analyzed
		self.assertTrue((conv2DLayers.N > 0).all(axis=None), "All {} conv2D layers have a non zero N".format(conv2DCount))
		self.assertTrue((conv2DLayers.M > 0).all(axis=None), "All {} conv2D layers have a non zero M".format(conv2DCount))

		nonConv2DLayers = d[d['layer_type']!="CONV2D"]
		nonConv2DCount = len(nonConv2DLayers)

		self.assertTrue(nonConv2DCount > 0, "VGG11 has non conv2D layers: {} found".format(nonConv2DCount))
		
		# Non Conv2D layers are NOT analyzed
		self.assertTrue((nonConv2DLayers.N == 0).all(axis=None), "All {} NON conv2D layers have a zero N".format(nonConv2DCount))
		self.assertTrue((nonConv2DLayers.M == 0).all(axis=None), "All {} NON conv2D layers have a zero M".format(nonConv2DCount))
    
	def test_density_fit(self):
		"""Test the fitted sigma from the density fit
		"""
		logger = logging.getLogger("imported_module")
		logger.setLevel(logging.CRITICAL)

		model = models.vgg11(pretrained=True)
		watcher = ww.WeightWatcher(model=model, logger=logger)
		results = watcher.analyze(layers = [10], alphas = True, spectralnorms=True, softranks=True, mp_fit = True)

		df = watcher.get_details()
		df = df.reset_index()
		self.assertAlmostEqual(df.loc[0, 'sigma_mp'], 1.00, places=2) #sigma_mp
		self.assertAlmostEqual(df.loc[0, 'numofSpikes'], 13) #numofSig
		#self.assertAlmostEqual(df.loc[0, 'sigma_mp'], 1.064648437) #sigma_mp
		#self.assertAlmostEqual(df.loc[0, 'numofSpikes'], 30.00) #numofSig
		#self.assertAlmostEqual(df.loc[0, 'ratio_numofSpikes'], 0.117647, places = 6)
		#self.assertAlmostEqual(df.loc[0, 'softrank_mp'], 0.203082, places = 6)

    
	def test_min_matrix_shape(self):
		"""Test that analyzes skips matrices smaller than  MIN matrix shape
		"""

	def test_max_matrix_shape(self):
		"""Test that analyzes skips matrices larger than  MAX matrix shape
		"""

	def test_max_matrix_shape(self):
		"""Test that analyzes skips matrices larger than  MAX matrix shape
		"""

	def test_layer_ids(self):
		"""Test that layer_ids start at 0, not 1
		"""

	def test_slice_ids(self):
		"""Test that slice_ids start at 0, not 1
		"""

	def test_slice_ids(self):
		"""Test that slice_ids start at 0, not 1
		"""

	def test_compute_alphas(self):
		"""Test that alphas are computed and values are within thresholds
		"""
		results = self.watcher.analyze(layers=[5], alphas=True)
		d = self.watcher.get_details(results=results)
		a = d.alpha.to_numpy()
		self.assertAlmostEqual(a[0],1.65014, places=4)
		self.assertAlmostEqual(a[1],1.57297, places=4)
		self.assertAlmostEqual(a[3],1.43459, places=4)

	def test_compute_spectral_norms(self):
		"""Test that spectral norms are computed and values are within thresholds
		"""
		logger = logging.getLogger("imported_module")
		logger.setLevel(logging.INFO)

		model = models.vgg11(pretrained=True)
		watcher = ww.WeightWatcher(model=model, logger=logger)

		results = self.watcher.analyze(layers=[5], alphas=True,  spectralnorms=True)#, normalize=False, glorot_fix=False)
		d = self.watcher.get_details(results=results)
		print(d)
		a = d.spectralnorm.to_numpy()
		self.assertAlmostEqual(a[0],20.2149, places=4)
		self.assertAlmostEqual(a[1],24.8158, places=4)
		self.assertAlmostEqual(a[2],19.3795, places=4)

	def test_compute_soft_rank(self):
		"""Test that soft ranks are computed and values are within thresholds
		"""

	def test_weighted_alpha(self):
		"""Test that weight alpha computed as expected and values are within thresholds
		"""

	def test_compound_averages(self):
		"""Test that compound averagesa computed as expected and values are within thresholds
		"""

	def test_normalize(self):
		"""Test that weight matrices are normalized as expected
		"""

	def test_return_eiegnavlues(self):
		"""Test that eigenvalues are returned in the result dict
		"""

	def test_runtime_warnings(self):
		"""Test that runtime warnings are still active
		"""
		import numpy as np
		print(np.sqrt(-1.0))
		assert(True)
		
        
        

if __name__ == '__main__':
	unittest.main()
