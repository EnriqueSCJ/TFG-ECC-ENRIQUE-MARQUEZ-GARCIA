declare module "react-katex" {
  import type { ComponentType, ReactNode } from "react";

  interface MathComponentProps {
    children?: ReactNode;
    math?: string;
  }

  export const BlockMath: ComponentType<MathComponentProps>;
  export const InlineMath: ComponentType<MathComponentProps>;
}
