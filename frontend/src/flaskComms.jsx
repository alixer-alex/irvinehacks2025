import { useEffect, useState } from "react";
import Graph from "graphology";
import { SigmaContainer, useLoadGraph } from "@react-sigma/core";
import "@react-sigma/core/lib/style.css";

const sigmaStyle = { height: "1080px", width: "1080px" };

// Component that load the graph
export const LoadGraph = () => {
    const loadGraph = useLoadGraph();
    const [data, setData] = useState(null);
    useEffect(() => {
        const graph = new Graph();
        fetch('../../backend/mutual_followers.json')
        .then(response => response.json())
        .then(data => setData(data))
        .catch(error => console.log(error))
        
        graph.addNode("first", { x: 0, y: 0, size: 15, label: "My first node", color: "#FA4F40" });
        loadGraph(graph);
        console.log(data);
    }, [loadGraph]);
    return null;
}

// Component that display the graph
export const DisplayGraph = () => {
  return (
    <SigmaContainer style={sigmaStyle}>
      <LoadGraph />
    </SigmaContainer>
  );
};
  export default DisplayGraph;