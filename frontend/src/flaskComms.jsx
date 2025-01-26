import { useEffect, useState } from "react";
import Graph from "graphology";
import { SigmaContainer, useLoadGraph } from "@react-sigma/core";
import "@react-sigma/core/lib/style.css";
import "@react-sigma/layout-noverlap";
import { useLayoutNoverlap } from "@react-sigma/layout-noverlap";
const sigmaStyle = { height: "1080px", width: "1080px" };



// Component that load the graph
export const LoadGraph = (username) => {
    const loadGraph = useLoadGraph();
    const { positions, assign } = useLayoutNoverlap();
    const [friends, setFriends] = useState(null);
    async function getData(){
      const url = "http://localhost:5000/api/" + username.username;
      try {
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error(`Response status: ${response.status}`);
        }
    
        const json = await response.json();
        console.log(json);
        return json;
        
      } catch (error) {
        console.error(error.message);
      }

    }
    useEffect(() => {
        const graph = new Graph();
        let temp = null;
        console.log(username.username)
        getData().then(
          data => {
            console.log(data.data);
            for (let key in data.data){
              console.log(key);
              graph.addNode(key, { x: 0, y: 0, size: 15, label: key, color: "##FF0000"});
            }
            for (let key in data.data){
              for(let i=0;i<data.data[key].length;i++){
                let value = data.data[key][i];
                console.log(graph.nodes())
                if(!graph.nodes().includes(value)){
                  graph.addNode(value, { x: 0, y: 0, size: 15, label: value, color: "##00FF00"});
                }
                graph.addEdge(key,value);
              }
            }
            loadGraph(graph);
            assign();
          }
          

        )
       
        
    }, [friends,assign,loadGraph]);
    return null;
}


// Component that display the graph
export const DisplayGraph = (props) => {
  return (
    <SigmaContainer style={sigmaStyle}>
      {console.log(props.username + "AAA")}
      <LoadGraph username={props.username}/>
    </SigmaContainer>
  );
};
  export default DisplayGraph;