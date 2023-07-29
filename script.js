
let canvas = document.getElementById('gameCanvas');
var settings;
let ctx = canvas.getContext('2d');
let CELLS = [];
let incomingDataChart;
let chartData = {time: [], s: [], i: [], r: [], d: [], dc: [], p: []};
let graphData = {time: [], adjacency: []}
var updateInterval;

let dataElementsIds = {
    textContent: ["susceptible", "infectious", "recovered", "totalPopulation"],

}

let dataElements = {
    textContent: dataElementsIds.textContent.reduce((o, key) => Object.assign(o, {[key]: document.getElementById(key)}), {})
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


function parentWidth(elem, coeff=0.9) {
    return coeff*elem.parentElement.clientWidth;
}

function parentHeight(elem, coeff=1) {
    return coeff*elem.parentElement.clientHeight;
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

async function updateData(){
    updateField().then(updateNumbers).then(incomingDataChart.update())
}

async function checkTaskCompletion(){
    let response = fetch("/check_task_completion")
                    .then(async r => {
                        let jsonMessage = await r.json()
                        if (!r.ok){
                            updateData();
                            console.error(jsonMessage);
                            clearInterval(updateInterval);
                            return;
                        }
                    }).catch();
    return;
}

// Function to update the game state (you can handle player movement and other updates here)
async function update() {
    updateData().then(checkTaskCompletion).catch(console.error);
}

async function startSimulation(){
    chartData  = {time: [], s: [], i: [], r: [], d: [], dc: [], p: []};   // Reset chartData
    renderChart();                                  // Create a new chart 
    fetch("/start_simulation");
}

function getSettings(){
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

async function sendData(data, endpointRoute, method="POST"){
    let requestOptions = {
        method: method, 
        headers: {
          "Content-Type": "application/json"
         
        },
        body: JSON.stringify(data), 
      };
    let response = fetch(endpointRoute, requestOptions);
    return response;
}

async function sendSettings(){
    settings = getSettings();
    let endpointRoute = "/set_settings";
    let response = sendData(settings, endpointRoute);
    return response
}


async function simulate(){
    sendSettings()
        .then(async r => {
            if (!r.ok){
                clearInterval(updateInterval);
                console.error(r);
                return;
            }
        })
        .then(startSimulation)
        .then(renderChart);
        clearInterval(updateInterval);
        updateInterval = setInterval(update, 500);

}

function updateElementTextContent(el, textContent){
    el.textContent = textContent;
    return el;
}

function pushDataToDataChart(variable, data){
    chartData[variable].push(data);
    return chartData;
}

function pushDataToGraphData(time, adjacency){
    graphData.time.push(time);
    graphData.adjacency.push(adjacency);
    return graphData;
}

function updateCycleCounter(cycleNumber){
    let timeT = document.getElementById("timeT");
    timeT.max = cycleNumber;
    timeT.value = cycleNumber;      // might be turned off
    return timeT;
}

async function updateNumbers(){
    let data;
    let jsonResponse;

    await fetch("/get_stats")
        .then(async response => {
            jsonResponse = await response.json();
            if (!response.ok){
                console.error(jsonResponse);
                clearInterval(updateInterval);
                return;
            }
            
            data = jsonResponse;
            let [time, susceptibleValue, infectiousValue, recoverValue, populationValue, d, dc, p] = data.stats;
            let adjacencyData = data.graph_data;
            
            updateElementTextContent(dataElements.textContent.susceptible, susceptibleValue);
            updateElementTextContent(dataElements.textContent.infectious, infectiousValue);
            updateElementTextContent(dataElements.textContent.recovered, recoverValue);
            updateElementTextContent(dataElements.textContent.totalPopulation, populationValue);
            
            pushDataToDataChart("time", time);
            pushDataToDataChart("i", infectiousValue);
            pushDataToDataChart("r", recoverValue);
            pushDataToDataChart("s", susceptibleValue);
            
            pushDataToDataChart("d", d);
            pushDataToDataChart("dc", dc);
            pushDataToDataChart("p", p);

            pushDataToGraphData(time, adjacencyData);
        
            let cycleNumber = adjacencyData.length - 1;
            updateCycleCounter(cycleNumber);
            getCycleNumber();
        });
    incomingDataChart.update();
    return data;
}

function getCycleNumber(){
    let timeT = document.getElementById("timeT");
    let realTime = document.getElementById("timeReal");
    realTime.textContent =  graphData.time[timeT.value];
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
            data: s,
        },
        {
            label: 'Recovered',
            backgroundColor: 'rgba(54, 162, 235, 1)',
            data: r,
        },
        {
            label: 'Infectious',
            backgroundColor: 'rgba(255, 99, 132, 1)',
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