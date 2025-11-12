//import Chart from 'chart.js';

let xValues;
let yValues;

// document.addEventListener('DOMContentLoaded', function () {
//     const button = document.querySelector('.open-button');
//     button.addEventListener('click', openCloseForm);
// });
// document.addEventListener('DOMContentLoaded', function () {
//     const button = document.querySelector('.form-container');
//     button.addEventListener('click', getDataToDisplay);
// });
let selectedValues;
function getDataToDisplay() {
    event.preventDefault()
    const backendUrl = 'http://127.0.0.1:5000'
    const selectElement = document.getElementById("devices");
    const selectedOptions = Array.from(selectElement.selectedOptions);
    if (selectedOptions.length > 2){
        alert("please only select 2")
        return
    }
    selectedValues = selectedOptions.map(option => String(option.value));
    console.log(selectedValues)
    let responseData;
    fetch(`${backendUrl}/historyPage`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(selectedValues)
    })
        .then(Response => Response.json())
        .then(data => {
            responseData = Object.values(data);
            console.log('response: ', responseData)
            formatDataForGraphing(responseData)
            graphIt()
        })
        .catch(error => {
            console.error('error:', error)
        })

};

function openCloseForm() {
    if (document.getElementById("myForm").style.display === "none") {
        document.getElementById("myForm").style.display = "block";
    } else {
        document.getElementById("myForm").style.display = "none";
    }
}
function formatDataForGraphing(data) {
    xValues = []
    yValues = []
    data.map(iterateForDetails)
}



function iterateForDetails(data, index, array) {
    for (const device of data) {
        xValues.push(device.date)
        if (device.status) {
            yValues.push(1)
        } else {
            yValues.push(0)
        }
    }
}



let historyChart;
function graphIt() {

    if (historyChart) {
        historyChart.destroy();
    }
    xValues = xValues.map(value => new Date(value));
    const locale = 'en-US';
    const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
    const formattedDates = xValues.map(date => date.toLocaleDateString(locale, options));


    var ctx = document.getElementById("historyChart")

    let data;
    let scales;
    if (xValues.length === 10) {
        data = {
            labels: xValues,
            datasets: [{
                fill: false,
                borderWidth: 2,
                backgroundColor: "rgba(0,0,255,1.0)",
                borderColor: "rgba(0,0,255,1)",
                data: yValues,
                stepped: true,
                label: selectedValues[0]
            }]
        }
        scales = {
            x: {
                type: "time",
                time: {
                    displayFormats: {
                        unit: "dd.MM.yy"
                    }
                },
                display: "true",

                title: {
                    display: "true",
                    text: "date"
                }

            },
            y: {
                ticks: { min: 0, max: 1 }
            },
        }
    }
    else if (xValues.length === 20) {
        var xyData = []
        for (let i = 0; i < 20; i++) {
            if (i <= 10) {
                xyData.push(
                    {
                        x: xValues[i],
                        y: yValues[i]
                    },
                )
            }
            else {
                xyData.push(
                    {
                        x: xValues[i],
                        y: yValues[i]
                    },
                )
            }
        }
        console.log(xyData)
        data = {
            labels: xValues,
            datasets: [{
                fill: false,
                borderWidth: 3,
                backgroundColor: "rgba(0,0,255,1.0)",
                borderColor: "rgba(0,0,255,0.5)",
                data: xyData.slice(0, 10),
                stepped: true,
                label: selectedValues[0]

            },
            {
                fill: false,
                borderWidth: 3,
                backgroundColor: "rgba(255,0,0,1.0)",
                borderColor: "rgba(255,0,0,0.5)",
                data: xyData.slice(10, 20),
                stepped: true,
                label: selectedValues[1]
            }]


        }
        scales = {
            x: {
                type: "time",
                time: {
                    displayFormats: {
                        unit: "day"
                    }
                },
                display: "true",

                title: {
                    display: "true",
                    text: "date"
                }

            },
            y: {
                type: 'linear',
                display: true,
                position: 'left',
            },
            y1: {
                type: 'linear',
                display: true,
                position: 'right',
            }
        }
    }
    historyChart = new Chart(ctx, {

        type: "line",
        data: data,
        options: {
            scales: scales,
            responsive: true,
            interaction: {
                mode: "index",
                intersect: false,
            },
            animation: {
                x: {
                    type: 'number',
                    easing: "easeInQuad",
                    duration: 100,
                    from: NaN,
                    delay(ctx) {
                        if (ctx.type !== 'data' || ctx.xStarted) {
                            return 0;
                        }
                        ctx.xStarted = true;
                        return ctx.index * 150;
                    }
                },
            },
            stacked: false,
        }
    },

    )
}
