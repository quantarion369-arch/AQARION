python -m py_compile causal_estimator.py test_causal_estimator.py timing_models.py
python -m unittest -v test_causal_estimator
python timing_models.py
