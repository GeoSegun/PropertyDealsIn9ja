
    $(document).ready(function () {
        $("#selected_state").on("change", function () {
            let stateVal = $("#selected_state").val();

            console.log(stateVal);
            $.ajax({
                url: "{% url 'enquiries:get_cities' %}",
                type: "post",
                data: {
                    "state": stateVal,
                    "csrfmiddlewaretoken": "{{csrf_token}}"
                },
                dataType: "json",
                before: function () {

                },
                success: function (res) {
                    let cities = res.cities;
                    console.log(res.success);
                    $('#selected_city').empty();
                    $.each(cities, function(index, item)
                    {
                        console.log(item);
                        $("#selected_city").append("<option value='"+item +"'>"+item +"</option>");
                    });

                    console.log("worked till here... \n\n\n");
                }
            })
        });
    });