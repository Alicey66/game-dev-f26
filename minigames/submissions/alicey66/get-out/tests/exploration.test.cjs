const {test}=require('node:test');
const assert=require('node:assert/strict');
const game=require('../engine.js');
const notebook=require('../exploration.js');
const level=require('../levels.js')[0];

test('records only distinct reached stopping positions, not crossed cells',()=>{
 const initial=game.create(level.board), next=game.step(initial,'down');
 const first=notebook.start(initial.position), stops=notebook.record(first,initial,next);
 assert.deepEqual(first,['0,0']);
 assert.deepEqual(stops,['0,0','1,0']);
 const across=game.step(next,'right');
 assert.deepEqual(notebook.record(stops,next,across),['0,0','1,0','1,4']);
});

test('a blocked move and a return to a known stop add nothing',()=>{
 const initial=game.create(level.board), first=notebook.start(initial.position);
 assert.equal(notebook.record(first,initial,game.step(initial,'up')),first);
 const down=game.step(initial,'down'), stops=notebook.record(first,initial,down);
 assert.equal(notebook.record(stops,down,game.step(down,'up')),stops);
});

test('undo retains discoveries; starting a new attempt resets them',()=>{
 const initial=game.create(level.board), next=game.step(initial,'down');
 const stops=notebook.record(notebook.start(initial.position),initial,next);
 assert.equal(notebook.record(stops,next,initial),stops);
 assert.deepEqual(stops,['0,0','1,0']);
 assert.deepEqual(notebook.start(initial.position),['0,0']);
 assert.deepEqual(notebook.start([2,3]),['2,3']);
});

test('a repeat-route simulation reaches the exit with four known stops',()=>{
 let state=game.create(level.board), stops=notebook.start(state.position);
 for(const action of ['down','up','down','right','down']){
  const next=game.step(state,action);stops=notebook.record(stops,state,next);state=next;
 }
 assert.equal(state.won,true);assert.equal(state.moves,5);
 assert.deepEqual(stops,['0,0','1,0','1,4','3,4']);
});
