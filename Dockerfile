# with this line we import python language.
FROM python:3.9
# copy the requirements.txt file in the image
COPY ./requirements.txt /app/requirements.txt
# the working directory will be the /app directory which can be
# found inside the python image
WORKDIR /app
# let's install the requirements (only Flask is needed)
RUN pip install -r requirements.txt
# we can now add our directory to the working directory
COPY . /app
# let's run the application
CMD [ "python","skidresultat-app.py" ]