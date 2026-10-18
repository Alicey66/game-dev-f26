/* Display-only memory. Never used by movement, legal actions, or the solver. */
(function(root){
 'use strict';
 function start(position){return [position.join(',')];}
 function record(stops, previous, next){
  const key=next.position.join(',');
  if(next===previous||stops.includes(key))return stops;
  return [...stops,key];
 }
 const api={start,record};
 if(typeof module!=='undefined'&&module.exports)module.exports=api;
 else root.GetOutExploration=api;
})(globalThis);
