function pushNodes(nodes, nodeList){
    nodes.forEach(node=> pushNode(node, nodeList))
    return nodeList;
}

function pushNode(node, nodeList){
    let myObj = {data:{id:node}}
    nodeList.push(myObj);
    return nodeList;
}

function pushEdge(sourceNode, targetNode, edgesList){
    let obj = {
        data: {
            id: sourceNode+targetNode,
            source: sourceNode,
            target: targetNode
        }
    }
    edgesList.push(obj);
    return edgesList;
}

function pushEdges(sourceNode, nodes, edgesList){
    nodes.forEach(node => {
        pushEdge(sourceNode, node, edgesList);
    })
    return edgesList
}


function createGraph(containerElement, elementsData, graphStyle){
    var cy = cytoscape(
        {
        container: containerElement,
        elements: elementsData,
        style: graphStyle,
        layout: {
            name: 'breadthfirst',
            directed: true,
            padding: 15
        }
    });
    return cy;
}

function dropNonExistentEdges(graphData, nodesIds){
    let newEdges = [];
    graphData.edges.forEach(edge => {
        target = edge.data.target;
        source = edge.data.source;
        if (nodesIds.indexOf(target) > -1 && nodesIds.indexOf(source)){
            newEdges.push(edge);
        }
    })
    return newEdges;
}

function getLargestDegreeGraph(graphData){
    let max = [0, 0];
    for (var key in graphData){
        if (graphData[key].length > max[0]){
        max[0] = graphData[key].length;
        max[1] = key;
    }
    }
    return max;
}

function getAllNodesIds(graphData){
    return Object.keys(graphData);
}

function getAllEdges(graphData){
    let nodes = getAllNodesIds(graphData);
    let edges = [];
    nodes.forEach(node => {
        pushEdges(node, graphData[node].map(nodeInfo=>nodeInfo[0].toString()), edges);
    })
    return edges;
}

function getAllNodes(graphData){
    let nodesIds = getAllNodesIds(graphData);
    let nodes = [];    
    nodesIds.forEach(nodeId => {
        let nodeObj = {
            data: {id: nodeId}
        };
        nodes.push(nodeObj);
    })
    return nodes;
}

function getGraphData(graphData){
    let nodesList = getAllNodes(graphData);
    let edgesList = getAllEdges(graphData);
    return {nodes: nodesList, edges: edgesList};
}



function changeNodesColor(graph, ids, color){
    let nodes = graph.filter('node'); 
    ids.forEach(id =>{
        let query = '[id = "{id}"]'.replace("{id}", id)
        nodes.filter(query).select().style("background-color", color);
    }
    )
}

function getSickIds(nodesIds, graphData){
    let sickIds = [];
    nodesIds.forEach(node => {
        let nodeInfos = graphData[node];
        nodeInfos.forEach(nodeInfo => {
            if (nodeInfo[1]){
                sickIds.push(nodeInfo[0]);
            }
        })

    });
    let uniqueSickIds = [...new Set(sickIds)]
    return uniqueSickIds;
}

function toggleContainerOpacity(){
    let container = document.getElementById("siteContainer");
    if (container.style.opacity != "1")
        container.style.opacity = "1";
    else 
        container.style.opacity = "0.05";
}

let cy;
function displayGraphAtTimeT(timeT, graph_data, layout="breadthfirst"){
    let adj = graph_data.adjacency[timeT];
    let nodesIds = getAllNodesIds(adj);
    let myGraphData = getGraphData(adj);
    myGraphData.edges = dropNonExistentEdges(myGraphData, nodesIds);
    graphContainer = document.getElementById("cy");
    cy = createGraph(graphContainer, myGraphData, style);   
    cy.layout({
        name: layout
    }).run();
    let sickIds = getSickIds(nodesIds, adj);
    changeNodesColor(cy, sickIds, "rgba(255, 99, 132, 1)");
    //graphContainer.classList.toggle("d-none");
    //toggleContainerOpacity();
    return cy; 
}


function displayGraph(){
    let timeT = Number(document.getElementById("timeT").value);
    cy = displayGraphAtTimeT(timeT, graphData);
}

function hideGraph(){
    cy = null;
    //graphContainer.classList.toggle("d-none");
    //toggleContainerOpacity();

}

let style = [
    {
        selector: 'node',
        style: {
            shape: 'hexagon',
            'background-color': 'rgba(255, 206, 86, 1)',
            label: 'data(id)'
        }
    }
];



/*
  
let graphStyle = [{
selector: 'node',
css: {
'content': 'data(id)',
'text-valign': 'center',
'text-halign': 'center',
'height': '60px',
'width': '60px',
'border-color': 'black',
'border-opacity': '1',
'border-width': '10px'
}
},
{
selector: '$node > node',
css: {
'padding-top': '10px',
'padding-left': '10px',
'padding-bottom': '10px',
'padding-right': '10px',
'text-valign': 'top',
'text-halign': 'center',
'background-color': '#bbb'
}
},
{
selector: 'edge',
css: {
'target-arrow-shape': 'triangle'
}
},
{
selector: ':selected',
css: {
'background-color': 'black',
'line-color': 'black',
'target-arrow-color': 'black',
'source-arrow-color': 'black'
}
}
]


*/