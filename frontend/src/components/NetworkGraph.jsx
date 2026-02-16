import React, { useEffect, useRef, useState } from 'react';
import ForceGraph2D from 'react-force-graph-2d';

const NetworkGraph = ({ data = { nodes: [], links: [] }, width = 600, height = 400 }) => {
    const fgRef = useRef();

    return (
        <div className="rounded-xl overflow-hidden border-2 border-pro-gray-800 shadow-neu-pressed">
            <ForceGraph2D
                ref={fgRef}
                width={width}
                height={height}
                graphData={data}
                nodeLabel="id"
                nodeColor={node => {
                    if (node.group === 'Artist') return '#00f0ff'; // Electric Cyan
                    if (node.group === 'Track') return '#ffffff';
                    if (node.group === 'Genre') return '#39ff14'; // Volt Green
                    return '#666';
                }}
                nodeRelSize={6}
                linkColor={() => '#333'}
                backgroundColor="#1a1a1a" // pro-black
            />
        </div>
    );
};

export default NetworkGraph;
