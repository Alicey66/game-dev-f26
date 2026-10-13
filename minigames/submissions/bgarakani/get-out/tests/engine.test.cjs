const {test}=require('node:test');
const assert=require('node:assert/strict');
const game=require('../engine.js');
const board=['S..#.', '.....', '.#...', '...E.', '.....'];
test('slides to a wall or border without mutating the input',()=>{
 const s=game.create(board);const next=game.step(s,'right');
 assert.deepEqual(next.position,[0,2]);assert.equal(next.moves,1);
 assert.deepEqual(s.position,[0,0]);assert.equal(s.moves,0);
 assert.deepEqual(game.step(s,'down').position,[4,0]);
});
test('blocked and unknown actions do not spend moves',()=>{
 const s=game.create(board);assert.deepEqual(game.step(s,'up'),s);
 assert.throws(()=>game.step(s,'teleport'),/direction/i);
});
test('reaching an exit mid-slide wins and terminal states cannot move',()=>{
 const s=game.create(['S.E..','.....','.....']);
 const won=game.step(s,'right');assert.deepEqual(won.position,[0,2]);
 assert.equal(won.won,true);assert.deepEqual(game.step(won,'down'),won);
});
test('solver finds the hand-checked shortest path and identifies unreachable exits',()=>{
 assert.deepEqual(game.solve(game.create(['S..','...','..E'])),['right','down']);
 assert.equal(game.solve(game.create(['S..','.E.','...'])),null);
});
test('invalid imported boards fail before play',()=>{
 for(const b of [[],['S.E','..'],['SSE'],['S..'],['S?E'],['S.E',42],Array(21).fill('S.E')]){
  assert.throws(()=>game.create(b));
 }
});
test('observations are detached and legal actions follow actual movement',()=>{
 const s=game.create(board);assert.deepEqual(game.legalActions(s),['right','down']);
 const obs=game.observe(s);obs.position[0]=99;obs.board[0]='broken';
 assert.deepEqual(s.position,[0,0]);assert.equal(s.board[0],board[0]);
});
test('every teaching board is solvable and its solution reaches the exit',()=>{
 const levels=require('../levels.js');
 for(const level of levels){
  const initial=game.create(level.board),solution=game.solve(initial);
  assert.ok(solution && solution.length>0,level.name);
  const final=solution.reduce((s,a)=>game.step(s,a),initial);
  assert.equal(final.won,true,level.name);
 }
});
test('budget tapers from twice optimal to exactly optimal',()=>{
 const square=n=>Array.from({length:n},(_,r)=>r===0?'S'+'.'.repeat(n-1):r===n-1?'.'.repeat(n-1)+'E':'.'.repeat(n));
 for(const [n,limit] of [[7,4],[24,3],[42,2]]){
  const s=game.create(square(n));assert.equal(s.minimumMoves,2);assert.equal(s.moveLimit,limit);
 }
 assert.throws(()=>game.create(square(43)));
});
test('last allowed move wins; exhaustion fails and freezes movement',()=>{
 let s=game.create(['S..','...','..E']);
 for(const a of ['right','left','right','left'])s=game.step(s,a);
 assert.equal(s.failed,true);assert.equal(s.won,false);
 assert.equal(game.step(s,'down'),s);assert.deepEqual(game.legalActions(s),[]);assert.equal(game.solve(s),null);
 let winning=game.create(['S..','...','..E']);
 for(const a of ['right','left','right','down'])winning=game.step(winning,a);
 assert.equal(winning.won,true);assert.equal(winning.failed,false);
 assert.equal(game.create(s.board).moves,0);
});
test('hints respect the remaining budget',()=>{
 let s=game.create(['S..','...','..E']);
 for(const a of ['right','left','right'])s=game.step(s,a);
 assert.deepEqual(game.solve(s),['down']);
 assert.equal(game.observe(s).moveLimit,4);
});
test('campaign grows every three levels and stops at 42',()=>{
 const levels=require('../levels.js');assert.equal(levels.length,108);
 for(const [i,level] of levels.entries()){
  const n=Math.min(42,7+Math.floor(i/3));assert.equal(level.board.length,n);
  assert.ok(level.board.every(row=>row.length===n));
 }
});

test('hints reject a reachable exit when the remaining budget is too small',()=>{
 const initial=game.create(['S.E....',...Array(6).fill('.......')]);
 const detour=game.step(initial,'down');
 assert.equal(initial.moveLimit,2);
 assert.equal(detour.moves,1);assert.equal(detour.failed,false);
 assert.deepEqual(game.solve({...detour,moveLimit:null}),['up','right']);
 assert.equal(game.solve(detour),null);
 assert.equal(game.step(detour,'left'),detour); // blocked input spends no budget
 const failed=game.step(detour,'up');assert.equal(failed.failed,true);
 assert.equal(game.solve(detour),null); // failed successor did not mutate history
 assert.deepEqual(game.solve(initial),['right']);
});
