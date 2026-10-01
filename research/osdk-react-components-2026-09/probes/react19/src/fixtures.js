export const textField = (defaultValue = 'Ada Lovelace') => ({
  type: 'field',
  definition: {
    fieldKey: 'employeeName', label: 'Employee name', fieldComponent: 'TEXT_INPUT',
    isRequired: true, fieldComponentProps: { defaultValue },
  },
});
export const booleanField = (isRequired, defaultValue = false) => ({
  type: 'field',
  definition: {
    fieldKey: 'enabled', label: 'Enabled', fieldComponent: 'RADIO_BUTTONS',
    isRequired, fieldComponentProps: {
      defaultValue, options: [{ label: 'True', value: true }, { label: 'False', value: false }],
    },
  },
});
