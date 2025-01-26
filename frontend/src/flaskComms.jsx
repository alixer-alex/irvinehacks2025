import { useEffect, useState } from "react";
import Graph from "graphology";
import { SigmaContainer, useLoadGraph } from "@react-sigma/core";
import "@react-sigma/core/lib/style.css";
import "@react-sigma/layout-noverlap";
import { useLayoutNoverlap } from "@react-sigma/layout-noverlap";
import "./App.css"
// const sigmaStyle = { height: "500px", width: "500px" };

// Component that load the graph
export const LoadGraph = (username) => {
    const loadGraph = useLoadGraph();
    const { positions, assign } = useLayoutNoverlap();
    const [data, setData] = useState(null);
    useEffect(() => {
        const graph = new Graph();
        // console.log(username.username)
        // fetch('/api/'+ username.username)
        // .then(response => response.json())
        // .then(data => setData(data))
        // .catch(error => console.log(error))
        
        // for(let key in data){
        //   graph.addNode(key, { x: 0, y: 0, size: 15, label: key, color: "#FA4F40" });
        // }
        graph.addNode("A", { x: 0, y: 0, size: 15, label: "A", color: "#FA4F40" });
        graph.addNode("B", { x: 0, y: 1, size: 15, label: "B", color: "blue" });
        graph.addNode("C", { x: 1, y: 0, size: 15, label: "C", color: "green" });
        graph.addEdge("A","C")
        graph.addEdge("B","C")
        loadGraph(graph);
        assign();
        console.log(data);
    }, [assign,loadGraph]);
    return null;
}


// Component that display the graph
export const DisplayGraph = (props) => {
  return (
    <div className="sigma_graph">
      <SigmaContainer>
      <LoadGraph username={props.username}/>
    </SigmaContainer>
    </div>
  );
};
  export default DisplayGraph;