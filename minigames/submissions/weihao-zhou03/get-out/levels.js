(function(root){
 const levels = [
    {name:'Cross traffic', prompt:'A moves sideways. B moves vertically. Borrow a stopping point from each.',
      board:['S.#.#..','..#.E..','#......','...#...','.......','...#.##','.......'],
      movers:[
        {path:[[4,0],[4,1],[4,2],[4,3]],index:1,direction:1},
        {path:[[1,6],[2,6],[3,6]],index:1,direction:1}
      ]},
    {name:'Three-way timing', prompt:'Three walls, one turn. Holding one wall in place lets the other two catch up.',
      board:['S#.#.##','.E###.#','.......','#......','....#..','.#.....','.##..##'],
      movers:[
        {path:[[2,3],[3,3],[4,3]],index:2,direction:-1},
        {path:[[5,2],[5,3],[5,4],[5,5]],index:0,direction:1},
        {path:[[2,1],[3,1],[4,1]],index:1,direction:-1}
      ]},
    {name:'Clockwork maze', prompt:'Plan the next two stops. Every wall can become a brake at the right moment.',
      board:['S.#.....','#..#.##.','........','#.#..#..','..#...#.','.......#','##...E#.','.##.....'],
      movers:[
        {path:[[2,2],[2,3],[2,4],[2,5]],index:1,direction:1},
        {path:[[1,1],[2,1],[3,1],[4,1]],index:0,direction:-1},
        {path:[[5,0],[5,1],[5,2]],index:1,direction:1}
      ]}
 ];
 if(typeof module!=='undefined'&&module.exports)module.exports=levels;else root.GetOutLevels=levels;
})(globalThis);
