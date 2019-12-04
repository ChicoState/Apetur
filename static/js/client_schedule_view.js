    // This map is used for fast look up when styling the photographers dates to be either green/red/yellow/gray depending on the booking status of that day
    var scheduleMap = new Map();
    // Create schedule map
    for(var i = 0; i < schedule_json_data.length; i++){
        scheduleMap.set(schedule_json_data[i]["date"],schedule_json_data[i]);
    }

    var clientCalendarEl = document.getElementById('client-calendar');
    var clientCalendar = new FullCalendar.Calendar(clientCalendarEl, {
        plugins: [ 'interaction' ,'dayGrid', 'timeGrid'],
        defaultView: 'dayGridMonth',
        dayRender: function(dayRenderInfo){
            var date = dayRenderInfo.date;
            var date_string = date.getFullYear() + "-"  + (date.getMonth() + 1) + "-" + date.getDate();
            if(scheduleMap.has(date_string)){
                let schedule = scheduleMap.get(date_string);
                if(schedule["fully_booked"] === true || schedule["num_bookings"] >= schedule["max_bookings"]){
                    schedule["fully_booked"] = true;
                    dayRenderInfo.el.classList.add("fully-booked");
                }
                else if(schedule["num_bookings"] === 0){
                    dayRenderInfo.el.classList.add("full-availability");
                }
                else if(schedule["num_bookings"] < schedule["max_bookings"]){
                    dayRenderInfo.el.classList.add("partial-availability");
                }
            }
            else{
                dayRenderInfo.el.classList.add("not-available");
            }

        },
        dateClick: function(dateClickInfo){
            let date_string = dateClickInfo.dateStr;
            if(scheduleMap.has(date_string)){
                let schedule = scheduleMap.get(date_string);
                if(!schedule["fully_booked"]){
                    var input_form_date_field = document.getElementById("schedule-event-form").event_date;
                    input_form_date_field.value = date_string;

                    var event_modal = document.getElementById("schedule-event-form-container");
                    event_modal.style.display = "block";
                }
            }
        }
    });

    window.onclick = function(event) {
        if (event.target.className === "modal") {
          event.target.style.display = "none";
        }
      }

    clientCalendar.render();