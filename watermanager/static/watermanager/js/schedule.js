$(window).load(function() {
    // page is now ready, initialize the calendar...
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth();  //January is 0
    var yyyy = today.getFullYear();

    var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

    document.getElementById("day").innerHTML = dd;
    document.getElementById("month").innerHTML = months[mm];
    document.getElementById("year").innerHTML = yyyy;

    var plant_ID = document.getElementById('plantID').value;
    var zip_code = document.getElementById("zip_code").value;

    $('#calendar').fullCalendar({
        dayClick: function(date, jsEvent, view) {
            month = date.month();
            day = date.date();
            year = date.year()
            document.getElementById("month").innerHTML = months[month];
            document.getElementById("month").value = month;
            document.getElementById("year").innerHTML = year;
            document.getElementById("year").value = year;
            document.getElementById("day").innerHTML = day;
            document.getElementById("day").value = day;
        },
        eventRender: function(event, element) {
            element.append( "<span class='closeon'>X</span>" );
            element.find(".closeon").click(function() {
               $('#calendar').fullCalendar('removeEvents',event._id);
               console.log(event.backgroundColor);
               console.log(event.start);
               console.log(event.start._i)
               $.ajax({
                        url: "/delete_watering_time",
                        data: {'plantID' : plant_ID, 'date' : event.start._i, 'color' : event.backgroundColor}
               });
            });
        }
    });

    var myEvents = '';
    $.ajax({
            url: "/add_events",
            data: {'plantID' : plant_ID},
            success: function( events ) {
                myEvents = jQuery.parseJSON(events);
                for (i = 0; i < myEvents.length; i++) {
                    var year = myEvents[i]['year'];
                    var day = myEvents[i]['day'];
                    var month = myEvents[i]['month'];
                    var wateringDate = new Date(year, month, day, 0, 0, 0, 0);
                    var userAdded = myEvents[i]['userAdded'];
                    var eventTitle = "";
                    var eventColor = ""; 
                    if (userAdded == true) {
                        eventTitle = "User Added Watering";
                        eventColor = 'blue';
                    }
                    else {
                        eventTitle = "AI Added Watering";
                        eventColor = 'red';
                    }
                    var watering = {
                        title: eventTitle,
                        backgroundColor: eventColor,
                        allDay: true,
                        editable: true,
                        start: wateringDate,
                        end: wateringDate
                    }
                    $('#calendar').fullCalendar('renderEvent', watering);
                }

            }
    });
    var addressUrl = "http://api.zippopotam.us/us/" + zip_code;
    var forecast_days = []; 
    var forecast_months = [];
    var forecast_years = [];
    var forecast_dates = []
    var forecast_total_precipitations = [];
    var forecast_highs = [];
    var forecast_lows = [];
    var forecast_humidities = [];
    $.ajax({
        url: addressUrl,
        cache: false,
        dataType: "json",
        type: "GET",
        success: function(result, success) {

            places = result['places'][0];

            var state  = places['state abbreviation'];
            document.getElementById("state").innerHTML = state;

            var city = places['place name'];

            document.getElementById("city").innerHTML = city;

            var url = "http://api.wunderground.com/api/9fcba2290be35824/forecast10day/q/" + state + "/" + city + ".json";

            $.getJSON(url, function(answer) {
                var monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
                var plantID = document.getElementById("plantID").value;
                var forecast = answer.forecast.simpleforecast.forecastday;
                for (i = 0; i < forecast.length; i++) {

                    var date = forecast[i].date;
                    
                    var day = date.day;
                    forecast_days.push(day);
                    
                    var month = date.month - 1; //January is the 0th month.
                    forecast_months.push(month);

                    var forecastDate = monthNames[month] + " " + day; 
                    forecast_dates.push(forecastDate);
                    
                    var year = date.year;
                    forecast_years.push(year);
                    
                    var total_precipitation = forecast[i].qpf_allday.in;
                    forecast_total_precipitations.push(total_precipitation);
                    
                    var high = forecast[i].high.fahrenheit;
                    forecast_highs.push(parseInt(high));
                    
                    var low = forecast[i].low.fahrenheit;
                    forecast_lows.push(parseInt(low));

                    var humidity = forecast[i].avehumidity;
                    forecast_humidities.push(parseInt(humidity));
                    
                }
                for (index = 0; index < 10; index++) {
                    $.ajax({
                        url: "/add_forecast",
                        data: {'plantID' : plant_ID, 'month' : forecast_months[index], 'day' : forecast_days[index], 'year' : forecast_years[index], 'high' : forecast_highs[index], 'low' : forecast_lows[index], 'total_precipitation' : forecast_total_precipitations[index], 'humidity' : forecast_humidities[index]},
                        type: "GET",
                        success: function(result, success) {
                            console.log("I love lamp");
                        }
                    });
                }
                $('#temperatures').highcharts({
                    chart: {
                        type: 'line'
                    },
                    title: {
                        text: '10-Day Forecast of High and Low Temperatures'
                    },
                    xAxis: {
                        categories: forecast_dates
                    },
                    yAxis: {
                        title: {
                            text: 'Temperature (°F)'
                        },
                        labels: {
                            formatter: function () {
                                return this.value + '°';
                            }
                        }
                    },
                    tooltip: {
                        crosshairs: true,
                        shared: true
                    },
                    plotOptions: {
                        dataLabels: {
                            enabled: true
                        },
                        spline: {
                            marker: {
                                radius: 4,
                                lineColor: '#666666',
                                lineWidth: 1
                            }
                        }
                    },
                    series: [{
                        name: 'High Temperatures',
                        marker: {
                            symbol: 'square'
                        },
                        data: forecast_highs

                    }, {
                        name: 'Low Temperatures',
                        marker: {
                            symbol: 'diamond'
                        },
                        data: forecast_lows
                    }]
                });
                $('#precipitation').highcharts({
                    chart: {
                        type: 'column'
                    },
                    title: {
                        text: '10-Day Forecast of Daily Precipitation'
                    },
                    xAxis: {
                        categories: forecast_dates
                    },
                    yAxis: {
                        title: {
                            text: 'Amount of Precipitation (inches)'
                        },
                        labels: {
                            formatter: function () {
                                return this.value + '"';
                            }
                        }
                    },
                    tooltip: {
                        crosshairs: true,
                        shared: true
                    },
                    plotOptions: {
                        spline: {
                            marker: {
                                radius: 4,
                                lineColor: '#666666',
                                lineWidth: 1
                            }
                        }
                    },
                    series: [{
                        name: 'Amount of Precipitation',
                        marker: {
                            symbol: 'square'
                        },
                        data: forecast_total_precipitations
                    }]
                });
                $('#humidity').highcharts({
                    chart: {
                        type: 'column'
                    },
                    title: {
                        text: '10-Day Forecast of Daily Average Humidity'
                    },
                    xAxis: {
                        categories: forecast_dates
                    },
                    yAxis: {
                        title: {
                            text: ' Average Humidity (%)'
                        },
                        labels: {
                            formatter: function () {
                                return this.value + '"';
                            }
                        }
                    },
                    tooltip: {
                        crosshairs: true,
                        shared: true
                    },
                    plotOptions: {
                        spline: {
                            marker: {
                                radius: 4,
                                lineColor: '#666666',
                                lineWidth: 1
                            }
                        }
                    },
                    series: [{
                        name: 'Average Humidity',
                        data: forecast_humidities
                    }]
                });
            });
            
        },
        error: function(result, success) {
            alert("It looks like the zip code that you have provided isn't a zip code for a US city. Please create a new plant with a valid US zip code so Water Manager can provide you forecasts and watering time recommendations.");
        }
    });
});

function addEvent() {
    var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    var year = document.getElementById("year").innerHTML;
    var month = document.getElementById("month").innerHTML;
    var day = document.getElementById("day").innerHTML;
    var plantID = document.getElementById("plantID").value;
    var monthNumber = months.indexOf(month);
    var startDate = new Date(year, monthNumber, day, 0, 0, 0, 0);
    var today = new Date();
    var dayToday = today.getDate();
    var monthToday = today.getMonth();
    var yearToday = today.getFullYear();
    if (year >= yearToday) {
        if (monthNumber >= monthToday) {
            if ((day >= dayToday) || (monthNumber > monthToday)) {
                var myEvent = {
                    title:" User Added Watering",
                    backgroundColor: 'blue',
                    allDay: true,
                    editable: true,
                    start: startDate,
                    end: startDate
                };
                $.ajax({url: "/add_watering_time",
                        data: {'plantID': plantID, 'year' : year, 'month' : monthNumber, 'day' : day},
                        success: function( comment ){
                            console.log("Event added");
                        }
                });
                $('#calendar').fullCalendar('renderEvent', myEvent);
            }
            else {
                alert("Please choose a date in the future to create an event.");
            }
        }
        else {
            alert("Please choose a date in the future to create an event.");
        }
    }
    else {
        alert("Please choose a date in the future to create an event.");
    }
}

function addAI(){
    var plantID = document.getElementById("plantID").value;
    var today = new Date();
    var dayToday = today.getDate();
    var monthToday = today.getMonth();
    var yearToday = today.getFullYear();
    var AIWaterings = '';
    $.ajax({url: "/add_AI",
            data: {'plantID' : plantID, 'dayToday' : dayToday, 'monthToday' : monthToday, 'yearToday' : yearToday},
            type : 'GET',
            success: function( events ){
                AIWaterings = jQuery.parseJSON(events);
                for (i = 0; i < AIWaterings.length; i++) {
                    var year = AIWaterings[i]['year'];
                    var day = AIWaterings[i]['day'];
                    var month = AIWaterings[i]['month'];
                    var wateringDate = new Date(year, month, day, 0, 0, 0, 0);
                    var userAdded = AIWaterings[i]['userAdded'];
                    var eventTitle = "";
                    var eventColor = ""; 
                    if (userAdded == true) {
                        eventTitle = "User Added Watering";
                        eventColor = 'blue';
                    }
                    else {
                        eventTitle = "AI Added Watering";
                        eventColor = 'red';
                    }
                    var watering = {
                        title: eventTitle,
                        backgroundColor: eventColor,
                        allDay: true,
                        editable: true,
                        start: wateringDate,
                        end: wateringDate
                    }
                    $('#calendar').fullCalendar('renderEvent', watering);
                }
            }
    });

}