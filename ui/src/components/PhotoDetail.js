import React, { useState } from 'react'
import styled from '@emotion/styled'
import useLocalStorageState from 'use-local-storage-state'

import history from '../history'
import ZoomableImage from './ZoomableImage'
import PhotoMetadata from './PhotoMetadata'

import { ReactComponent as ArrowBackIcon } from '../static/images/arrow_back.svg'
import { ReactComponent as InfoIcon } from '../static/images/info.svg'
import { ReactComponent as CloseIcon } from '../static/images/close.svg'

const Container = styled('div')`
  width: 100vw;
  height: 100vh;
  background-color: #1b1b1b;

  .content {
    width: 110vw;
    height: 100vh;
    overflow: auto;
    position: fixed;
    z-index: 10;
    top: 0;
    left: 0;
  }

  .backIcon {
    position: absolute;
    top: 10px;
    left: 10px;
    cursor: pointer;
    z-index: 10;
  }
  .PhotoDetail .backIcon {
    top: 40px;
  }
  .backIcon svg {
    filter: invert(0.9);
  }
  .showDetailIcon {
    position: absolute;
    right: 10px;
    top: 10px;
    filter: invert(0.9);
    cursor: pointer;
    z-index: 10;
  }

  /* When two boxes can no longer fit next to each other */
  @media all and (max-width: 500px) {
    .metadata .boxes .box {
      width: 100%;
    }
    .metadata .boxes .histogram {
      margin-right: 40px;
    }
    .metadata .boxes .map {
      margin-right: 40px;
    }
  }
`

const PhotoDetail = ({ photoId, photo, refetch }) => {
  const [showBoundingBox, setShowBoundingBox] = useLocalStorageState(
    'showObjectBoxes',
    true
  )
  const [showPhotoMetadata, setShowPhotoMetadata] = useState(false)

  let boxes = photo.objectTags.map((objectTag) => {
    return {
      name: objectTag.tag.name,
      positionX: objectTag.positionX,
      positionY: objectTag.positionY,
      sizeX: objectTag.sizeX,
      sizeY: objectTag.sizeY,
    }
  })

  const url = `/thumbnailer/photo/3840x3840_contain_q75/${photoId}/`

  return (
    <Container>
      <ZoomableImage url={url} boxes={showBoundingBox && boxes} />
      <PhotoMetadata
        photo={photo}
        show={showPhotoMetadata}
        refetch={refetch}
        showBoundingBox={showBoundingBox}
        setShowBoundingBox={setShowBoundingBox}
      />
      <div className="backIcon" title="[Esc] key to go back to photo list">
        <ArrowBackIcon alt="Close" onClick={history.goBack} />
      </div>
      {showPhotoMetadata && (
        <CloseIcon
          className="showDetailIcon"
          height="30"
          width="30"
          onClick={() => setShowPhotoMetadata(!showPhotoMetadata)}
        />
      )}
      {!showPhotoMetadata && (
        <InfoIcon
          className="showDetailIcon"
          height="30"
          width="30"
          onClick={() => setShowPhotoMetadata(!showPhotoMetadata)}
        />
      )}
    </Container>
  )
}

export default PhotoDetail
