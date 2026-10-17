// Rebuild the fixed campaign with: node generate-levels.cjs
// Seeded random walls; keep only boards with solver-verified routes.
const fs=require('node:fs');
const game=require('./engine.js');
const reference=require('../../../get-out/levels.js');
let seed=20261012;
function random(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296;}
const levels=reference.slice(0,3);
for(let i=3;i<108;i++){
 const size=Math.min(42,7+Math.floor(i/3));
 let board;
 for(let attempt=0;attempt<10000;attempt++){
  const rows=Array.from({length:size},()=>Array.from({length:size},()=>random()<0.22?'#':'.'));
  rows[0][0]='S';rows[size-1][size-1]='E';
  const candidate=rows.map(row=>row.join(''));
  const state=game.create(candidate);
  if(state.minimumMoves!==null && state.minimumMoves>=4){board=candidate;break;}
 }
 if(!board)throw new Error(`Could not generate level ${i+1}`);
 levels.push({name:`Growing challenge ${i+1}`,prompt:'Plan your stopping points before you slide.',board});
}
fs.writeFileSync(require('node:path').join(__dirname,'levels.js'),`(function(root){\n const levels = ${JSON.stringify(levels,null,2)};\n if(typeof module!=='undefined'&&module.exports)module.exports=levels;else root.GetOutLevels=levels;\n})(globalThis);\n`);
