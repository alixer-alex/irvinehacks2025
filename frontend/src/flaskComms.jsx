import { useEffect, useState } from "react";
import Graph from "graphology";
import { SigmaContainer, useLoadGraph } from "@react-sigma/core";
import "@react-sigma/core/lib/style.css";
import "@react-sigma/layout-noverlap";
import { useLayoutNoverlap } from "@react-sigma/layout-noverlap";
//const sigmaStyle = { height: "500px", width: "500px" };

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
        // console.log(username.username)
        // fetch('/api/'+ username.username)
        // .then(response => response.json())
        // .then(data => setData(data))
        // .catch(error => console.log(error))
        
        console.log(username.username)
        getData().then(
          data => {
            
            for (let key in data){
              console.log(key);
              graph.addNode(key, { x: 0, y: 0, size: 15, label: key, color: "##FF0000"});
            }
            for (let key in data){
              for(let i=0;i<data[key].length;i++){
                let value = data[key][i];
                console.log(graph.edges())
                if(!graph.nodes().includes(value)){
                  graph.addNode(value, { x: 0, y: 0, size: 15, label: value, color: "##00FF00"});
                }
                try{
                  graph.addEdge(key,value);
                }
                catch{

                }
                console.log(graph.edges())
              }
            }
            loadGraph(graph);
            assign();
          }
          

        )
       
        
    }, [friends,assign,loadGraph]);
    return null;
}

export const DisplayGraph = (props) => {
  return (
  <div className="sigma_graph" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
    <SigmaContainer>
    <LoadGraph username={props.username}/>
    </SigmaContainer>
  </div>
);
};
export default DisplayGraph;