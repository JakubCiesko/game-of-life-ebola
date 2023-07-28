
let canvas = document.getElementById('gameCanvas');

var settings;

resizeCanvasToDisplaySize(canvas);

let ctx = canvas.getContext('2d');


let CELLS = [];

let incomingDataChart;
let chartData = {time: [], s: [], i: [], r: []}; 
let updateBool = true;

function resizeCanvasToDisplaySize(canvas) {
    // look up the size the canvas is being displayed
    const width = canvas.clientWidth;
    const height = canvas.clientHeight;
 
    // If it's resolution does not match change it
    if (canvas.width !== width || canvas.height !== height) {
      canvas.width = width;
      canvas.height = height;
      return true;
    }
 
    return false;
 }



function createCell(x, y, color, width=2, height=2){
    let cell = {
        x: x, 
        y: y, 
        width: width,
        height: height, 
        color: color
    };
    return cell
}


function parentWidth(elem) {
    return 0.9*elem.parentElement.clientWidth;
}

function parentHeight(elem) {
    return elem.parentElement.clientHeight;
}

function draw(thisIterationCells) {
    let drawBool = false;
    if (thisIterationCells.length > 0){
        
        let actualWidth = canvas.width;
        let actualHeight = canvas.height;
        let setWidth = settings.windowWidth;
        let setHeight = settings.windowHeight;
        let setHeightWidthRatio = setHeight/setWidth; 
        
        ctx.canvas.width  = parentWidth(canvas);
        ctx.canvas.height = setHeightWidthRatio*ctx.canvas.width;
        
        let xDisplayRatio = actualWidth/setWidth;
        let yDisplayRatio = actualHeight/setHeight;

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        thisIterationCells.forEach(cell => {
            let x = cell.x * xDisplayRatio;
            let y = cell.y * yDisplayRatio;
            ctx.fillStyle = cell.color;
            ctx.fillRect(x, y, xDisplayRatio, yDisplayRatio);
        })
        drawBool = true;
    }
    return drawBool;
}

function getCellsInfo(){
    let cellsInfo;
    let response = fetch("/get_cells")
                    .then(async r => {
                        cellsInfo = await r.json();
                        if (!r.ok){
                            console.error(cellsInfo);
                            clearInterval(updateInterval);
                            return;
                        }
                    });
                    
    return cellsInfo;
}

async function createCells(){
    
    let canvasWidth = 5
    let canvasHeight = 4;
    let cellsInfo;
    let insideCells = [];
    CELLS = [];
    let response = fetch("/get_cells")
                    .then(async r => {
                        cellsInfo = await r.json();
                        if (!r.ok){
                            console.error(cellsInfo);
                            clearInterval(updateInterval);
                            return;
                        }
                    })
                    .then(r => {
                        if (cellsInfo.length > 0){
                            cellsInfo.forEach(cellInfo => {
                                let x = cellInfo.position[0]*canvasWidth;
                                let y = cellInfo.position[1]*canvasHeight;
                                color = cellInfo.ebola? "rgba(255, 99, 132, 1)": "rgba(255, 206, 86, 1)";
                                CELLS.push(createCell(x, y, color));
                                insideCells.push(createCell(x, y, color));
                            })
                        }
                    }).catch(console.log);
    return insideCells;
}


async function updateField(){
    let cellsInfo;
    let response = fetch("/get_cells")
                    .then(async r => {
                        cellsInfo = await r.json();
                        if (!r.ok){
                            console.error(cellsInfo);
                            clearInterval(updateInterval);
                            return;
                        }
                    })
                    .then(r => {
                        if (cellsInfo.length > 0){
                            CELLS = [];
                            cellsInfo.forEach(cellInfo => {
                                let x = cellInfo.position[0];
                                let y = cellInfo.position[1];

                                color = cellInfo.ebola? "rgba(255, 99, 132, 1)": "rgba(255, 206, 86, 1)";
                                CELLS.push(createCell(x, y, color));
                            })
                        }
                    }).catch(console.log);
    draw(CELLS);
    return;
} 

// Function to update the game state (you can handle player movement and other updates here)
async function update() {
    
    updateField().then(updateNumbers).then(x => incomingDataChart.update());
    
}

async function startSimluation(){
    chartData = {time: [], s: [], i: [], r: []};
    renderChart();
    fetch("/start_simluation");
}

function getData(){
    let initialInfectedNumber = document.getElementById("initialInfectedNumber").value;
    let totalNumberOfCells = document.getElementById("totalNumberOfCells").value;
    let ebolaSwitch = document.getElementById("ebolaSwtich").checked;
    let ebolaLife = document.getElementById("ebolaLife").value;
    let ebolaInfection = document.getElementById("ebolaInfection").value;
    let survive =  document.getElementById("survive").value;
    let underpopulation =  document.getElementById("underPopulation").value;
    let overpopulation =  document.getElementById("underPopulation").value;
    let width = document.getElementById("width").value;
    let height = document.getElementById("height").value;

    let data = {
        initialInfectedNumber: initialInfectedNumber, 
        totalNumberOfCells: totalNumberOfCells,
        ebola: ebolaSwitch,
        ebola_life: ebolaLife,
        ebola_infection: ebolaInfection,
        survive: survive,
        underpopulation: underpopulation, 
        overpopulation: overpopulation,
        windowWidth: width,
        windowHeight: height,
    };
    return data
}

async function sendSettings(){
    settings = getData()
    requestOptions = {
        method: "POST", 
        headers: {
          "Content-Type": "application/json"
         
        },
        body: JSON.stringify(settings), 
      };
    let response = fetch("/set_settings", requestOptions);
    return response
}


var updateInterval;
async function simulate(){
    updateBool = true;
    cells = [];
    sendSettings()
        .then(async r => {
            if (!r.ok){
                clearInterval(updateInterval);
                console.error(r);
                return ;
            }
        })
        .then(startSimluation)
        .then(renderChart);
        //.then(update);
        updateInterval = setInterval(update, 500);

}

async function updateNumbers(){
    let data;
    let susceptible = document.getElementById("susceptible");
    let infectious = document.getElementById("infectious");
    let recovered = document.getElementById("recovered");
    let population = document.getElementById("totalPopulation");
    let jsonResponse;
    await fetch("/get_stats")
        .then(async response => {
            jsonResponse = await response.json();
            if (!response.ok){
                console.error(jsonResponse);
                //updateBool=false;
                return;
            }
            data = jsonResponse;
            susceptible.textContent = jsonResponse[1];
            infectious.textContent = jsonResponse[2];
            recovered.textContent = jsonResponse[3];
            population.textContent = jsonResponse[4];
            chartData.time.push(jsonResponse[0]);
            chartData.i.push(jsonResponse[2]);
            chartData.r.push(jsonResponse[3]);
            chartData.s.push(jsonResponse[1]);
        });
    
    return data;
}

function renderChart() {
    let data = chartData;
    let labels = data.time;
    let i = data.i;
    let r = data.r;
    let s = data.s;
    
    let ctx = document.getElementById('dataChart').getContext('2d');
    ctx.canvas.width  = window.innerWidth;
    ctx.canvas.height = window.innerHeight;
    if (incomingDataChart) {
        // If the chart instance exists, destroy it before rendering the new chart
        incomingDataChart.destroy();
    }
    incomingDataChart = new Chart(ctx, {
        type: 'line', // You can choose a different chart type here (line, pie, etc.)
        data: {
        labels: labels,
        datasets: [{
            label: 'Susceptible',
            backgroundColor: 'rgba(255, 206, 86, 1)',
            //borderColor: 'rgba(75, 192, 192, 1)',
            //borderWidth: 1,
            data: s,
        },
        {
            label: 'Recovered',
            backgroundColor: 'rgba(54, 162, 235, 1)',
            //borderColor: 'rgba(75, 192, 192, 1)',
            //borderWidth: 1,
            data: r,
        },
        {
            label: 'Infectious',
            backgroundColor: 'rgba(255, 99, 132, 1)',
            //borderColor: 'rgba(75, 192, 192, 1)',
            //borderWidth: 1,
            data: i,
        } 
        ]
        },
        options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
            beginAtZero: true
            }
        }
        }
    });
}