import React from 'react';
import { FormControl, FormErrorMessage, FormHelperText, FormLabel } from '@chakra-ui/react';
import { useRecoilValue } from 'recoil';
import PassengerCount from './PassengerCount';
import YearSelector from './YearSelector';
import { predictionYearError } from '../../state/atoms';

const Form = () => {
  const isError = useRecoilValue(predictionYearError);
  return (
    <>
      <FormControl isRequired>
        <FormLabel htmlFor="passengerCount">Passenger Count</FormLabel>
        <PassengerCount />
      </FormControl>
      <FormControl isRequired isInvalid={isError}>
        <FormLabel htmlFor="year">Year</FormLabel>
        <YearSelector />
        {!isError ? (
          <FormHelperText>That&apos;s the year we&apos;ll compare to current prices</FormHelperText>
        ) : (
          <FormErrorMessage>Year is required.</FormErrorMessage>
        )}
      </FormControl>
    </>
  );
};

export default Form;
