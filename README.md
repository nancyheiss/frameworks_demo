# frameworks_demo
Test Automation Framework Demo for QA/LA

This test automation framework demo code shows you:
  1. How to use the Python Selenium bindings to run a simple web page test
  2. Basic usage of the Page Object Model design pattern
  3. How to incorporate data-driven testing using nose_parameterized
  4. How to integrate with SauceLabs and Jenkins

Since these tests will run at SauceLabs, you can take advantage of nose multiprocessing capability and run your tests in parallel with the following command:

nosetests -v PythonOrgSearch.py --processes=4 --process-timeout=120

Shout out to the folks who developed the Python Selenium bindings and provided a wonderful tutorial on Page Objects, where most of this code originated:

http://selenium-python.readthedocs.io/page-objects.html

(PS - The slides from the presentation are in the Test Automation Frameworks.key file)
