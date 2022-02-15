import React from 'react';
import { Box } from '@chakra-ui/react';
import { Marker as MapboxMarker, MarkerDragEvent } from 'react-map-gl';
import { useRecoilState } from 'recoil';
import PropTypes from 'prop-types';
import { markerPositions } from '../../state/atoms';

type MarkerProps = {
  type: string;
  marker: string;
};

const Marker = ({ type, marker }: MarkerProps) => {
  const [coords, setCoords] = useRecoilState(markerPositions(type));

  const onHandleDrag = (e: MarkerDragEvent) => {
    setCoords({ lng: e.lngLat.lng, lat: e.lngLat.lat });
  };

  return (
    <MapboxMarker latitude={coords.lat} longitude={coords.lng} onDrag={onHandleDrag} draggable>
      <Box w="20px" h="34px" bgImage={marker} />
    </MapboxMarker>
  );
};

Marker.propTypes = {
  type: PropTypes.string.isRequired,
  marker: PropTypes.string.isRequired,
};

export default Marker;
