/* Synthetic behavior only: not a human playtest or evidence of player feelings. */
const game=require('./engine.js');
const levels=require('./levels.js');
const notebook=require('./exploration.js');
function randomSource(seed){
 let value=seed>>>0;
 return ()=>{value=(Math.imul(value,1664525)+1013904223)>>>0;return value/4294967296;};
}
function episode(board,seed,useNotebook){
 const random=randomSource(seed);
 let state=game.create(board),stops=notebook.start(state.position),revisits=0;
 for(let attempt=0;attempt<200&&!state.won;attempt++){
  const legal=game.legalActions(state);
  if(!legal.length)break;
  // Perfect-information one-step lookahead, not a model of human perception.
  const fresh=useNotebook?legal.filter(action=>!stops.includes(game.step(state,action).position.join(','))):[];
  const choices=fresh.length?fresh:legal;
  const next=game.step(state,choices[Math.floor(random()*choices.length)]);
  if(stops.includes(next.position.join(',')))revisits++;
  stops=notebook.record(stops,state,next);state=next;
 }
 return {won:state.won,moves:state.moves,revisits,distinctStops:stops.length};
}
function summarize(runs){
 const completed=runs.filter(run=>run.won);
 const mean=(rows,key)=>rows.length?Number((rows.reduce((sum,row)=>sum+row[key],0)/rows.length).toFixed(2)):null;
 return {episodes:runs.length,completed:completed.length,meanMovesAllEpisodes:mean(runs,'moves'),
  meanMovesCompletedEpisodes:mean(completed,'moves'),meanRevisitsAllEpisodes:mean(runs,'revisits')};
}
const report={
 evidenceType:'automated simulation, not human play',
 setup:'100 seeds (1–100) per board and policy; at most 200 legal moves; no hints or solver calls inside episodes.',
 policies:{baseline:'Uniformly choose a legal direction.',notebook:'Prefer legal directions ending at unvisited stops, then choose uniformly; requires perfect-information one-step lookahead.'},
 boards:levels.map(level=>({name:level.name,shortestRoute:game.solve(game.create(level.board)),
  baseline:summarize(Array.from({length:100},(_,i)=>episode(level.board,i+1,false))),
  notebook:summarize(Array.from({length:100},(_,i)=>episode(level.board,i+1,true)))})),
 limitation:'These policies have different action selection rules. Their comparison tests a hypothetical use of the notebook, not the causal effect of displaying dots to humans. It cannot establish understanding, confidence, fun, or completion time.'
};
console.log(JSON.stringify(report,null,2));
