
for /l %%x in (1,1,100000) do (
	F:\SSeid\anaconda\Anaconda2\envs\gl-env\python.exe compute.py
	python send_submission.py -u wniemkowski -p wsxzse01 -f result.csv
	timeout 1000
	)

pause