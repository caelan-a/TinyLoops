import React, { Component } from 'react';
import Loop from './Loop'
import Grid from '@material-ui/core/Grid';
import './Loop.css';
import * as Mousetrap from 'mousetrap';
import FiberManualRecordIcon from '@material-ui/icons/FiberManualRecord';
import IconButton from '@material-ui/core/IconButton';

export default class ProgressRing extends React.Component {


    constructor(props) {
        super(props);

        this.state = { loops: this.props.loops, recording: false};
        this.addLoop = this.addLoop.bind(this)


    }

    componentDidMount() {
        Mousetrap.bind('space', this.record);
    }

    record() {
        navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
          const mediaRecorder = new MediaRecorder(stream);
          mediaRecorder.start();
      
          const audioChunks = [];
          mediaRecorder.addEventListener("dataavailable", event => {
            audioChunks.push(event.data);
          });
      
          mediaRecorder.addEventListener("stop", () => {
            const audioBlob = new Blob(audioChunks);
            const audioUrl = URL.createObjectURL(audioBlob);
            const audio = new Audio(audioUrl);
            audio.play();
          });
      
          setTimeout(() => {
            mediaRecorder.stop();
          }, 3000);
        });
    }

    addLoop() {
        let loops = this.state.loops;
        loops.push('a');
        this.setState({ loops: loops });
    }


    render() {
        var buildLoops = this.state.loops.map(function (loop, i) {
            let active = i == 0 ? true : false;
            let name = i == 0 ? "Main" : i;

            return (
                <Grid key={i} item>
                    <Loop radius="50" stroke="6" progress="75" title={name} isActive={active} playing={false}></Loop>
                </Grid>
            );
        });



        return (
            <div  >

                <Grid container >
                    <Grid item xs={12}>
                        <Grid container justify="center" spacing='2'>
                            {this.state.loops.length == 0 &&
                                <div >
                                    <p style={{ color: "white" }}>
                                        Record
                                    </p>
                                    <IconButton color="primary" aria-label="mute" component="span" onClick={this.addLoop}>

                                        <FiberManualRecordIcon style={{
                                            width: 60,
                                            height: 60,
                                        }} /></IconButton>
                                </div>}



                            {buildLoops}

                        </Grid>

                    </Grid></Grid>

            </div >
        );
    }


}


