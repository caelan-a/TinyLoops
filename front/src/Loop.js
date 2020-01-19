import React, { Component } from 'react';
import Slider from '@material-ui/core/Slider';
import VolumeMuteIcon from '@material-ui/icons/VolumeMute';
import MusicOffIcon from '@material-ui/icons/MusicOff';
import PauseIcon from '@material-ui/icons/Pause';
import PlayArrowIcon from '@material-ui/icons/PlayArrow';
import IconButton from '@material-ui/core/IconButton';
import MusicNoteIcon from '@material-ui/icons/MusicNote';
import ClearIcon from '@material-ui/icons/Clear';
import './Loop.css';

var divStyle = {
    height: '100px',
    padding: '30px'
};


export default class ProgressRing extends React.Component {


    constructor(props) {
        super(props);

        const { radius, stroke, progress, isActive, title } = this.props;

        this.togglePlaying = this.togglePlaying.bind(this);

        this.state = { title: this.props.title, playing: this.props.playing };

        this.normalizedRadius = radius - stroke * 2;
        this.circumference = this.normalizedRadius * 2 * Math.PI;
    }

    togglePlaying() {
        this.setState(state => ({
            playing: !state.playing
        }));
    }

    render() {
        const { radius, stroke, progress } = this.props;
        const strokeDashoffset = this.circumference - progress / 100 * this.circumference;

        function buidActiveLED(isActive) {
            if (isActive) {
                return (
                    <div className='orb_on'>
                    </div>
                );
            } else {
                return (
                    <div className='orb_off'>
                    </div>
                );
            }
        }

        function buildControls(title, playing, togglePlaying) {
            if (title != 'Main') {
                return (
                    <div>
                        <div style={{ paddingBottom: 10 }}>
                            <IconButton color="primary" aria-label="mute" component="span" onClick={togglePlaying}>
                                {playing && <MusicNoteIcon />}
                                {!playing && <MusicOffIcon />}

                            </IconButton>

                        </div>
                        <IconButton color="primary" aria-label="delete" component="span">
                            <ClearIcon />
                        </IconButton>


                    </div>
                );
            } else {
                return (<div>
                    <div style={{ paddingBottom: 10 }}>
                        <IconButton color="primary" aria-label="mute" component="span" onClick={togglePlaying}>
                            {!playing && <PlayArrowIcon />}
                            {playing && <PauseIcon />}
                        </IconButton>


                    </div>
                </div>);
            }
        }
        return (
            <div >
                {buidActiveLED(this.props.isActive)}
                <p className='glow'>
                    {this.props.title}
                </p>
                <svg
                    viewBox="25 25 100 100"
                    height={radius * 2}
                    width={radius * 2}
                >
                    <defs>
                        <filter id="dropGlow" height="150%" width="150%" filterUnits="userSpaceOnUse" x="-.25" y="-.25">
                            <feGaussianBlur id="feGaussianBlur5384" in="SourceAlpha" stdDeviation="15.000000" result="blur" />
                            <feColorMatrix id="feColorMatrix5386" result="bluralpha" type="matrix" values="-1 0 0 0 1 0 -1 0 0 1 0 0 -1 0 1 0 0 0 0.800000 0 " />
                            <feOffset id="feOffset5388" in="bluralpha" dx="0.000000" dy="0.000000" result="offsetBlur" />
                            <feMerge id="feMerge5390">
                                <feMergeNode id="feMergeNode5392" in="offsetBlur" />
                                <feMergeNode id="feMergeNode5394" in="SourceGraphic" />
                            </feMerge>
                        </filter>
                    </defs>
                    <circle

                        stroke='white'
                        padding='100px'


                        fill="transparent"
                        strokeWidth={stroke}
                        strokeDasharray={this.circumference + ' ' + this.circumference}
                        style={{ strokeDashoffset }}
                        stroke-width={stroke}
                        r={this.normalizedRadius}
                        cx={radius * 1.5}
                        cy={radius * 1.5}
                    />
                </svg>
                <div style={divStyle}>
                    <Slider
                        background='lightBlue'
                        orientation="vertical"
                        defaultValue={50}
                        aria-labelledby="vertical-slider"
                    />

                </div>
                {buildControls(this.state.title, this.state.playing, this.togglePlaying)}
            </div >
        );
    }


}


